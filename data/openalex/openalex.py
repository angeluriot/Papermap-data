import os, io, json, gzip, requests
from typing import Any
from data.utils import *


def import_raw(url: str, output: str):
	if os.path.exists(output):
		return

	with open(output, 'w', encoding='utf-8') as out_file:
		manifest_url = url + '/manifest'
		resp = requests.get(manifest_url)
		resp.raise_for_status()
		manifest = resp.json()

		for entry in manifest.get('entries', []):
			s3_url = entry.get('url')
			file_url = s3_url.replace('s3://openalex', 'https://openalex.s3.amazonaws.com')
			r = requests.get(file_url, stream=True)
			r.raise_for_status()

			with gzip.GzipFile(fileobj=r.raw) as gz:
				reader = io.TextIOWrapper(gz, encoding='utf-8')

				for line in reader:
					line = line.strip()

					if not line:
						continue

					out_file.write(line + '\n')


def process_publishers(verbose: bool = False) -> tuple[
	dict[str, dict[str, Any]],
 	dict[str, dict[str, Any]],
	dict[str, dict[str, Any]],
]:
	if verbose:
		print('Publishers...')

	raw_path = 'data/openalex/raw/publishers.jsonl'
	output_path = 'data/openalex/publishers.json'

	if verbose:
		print('  Download...')

	if not os.path.exists(raw_path):
		import_raw('https://openalex.s3.amazonaws.com/data/publishers', raw_path)

	if verbose:
		print('  Process...')

	if os.path.exists(output_path):
		os.remove(output_path)

	publishers = {}
	sub_publishers = {}
	institutions = {}

	with open(raw_path, 'r', encoding='utf-8') as in_file:
		for line in in_file.readlines():
			line = line.strip()

			if not line:
				continue

			raw_entry = json.loads(line)
			id = clean_id(get_string(raw_entry, 'id'))
			title = clean_text(get_string(raw_entry, 'display_name'))

			if id == '' or title == '':
				continue

			titles = clean_list(get_list(raw_entry, 'alternate_titles'))
			lineage = [clean_id(i) for i in get_list(raw_entry, 'lineage')]
			p = clean_id(get_string(get_dict(raw_entry, 'parent_publisher'), 'id'))

			if id in lineage:
				lineage.remove(id)

			if len(lineage) == 0:
				parent = ''

			elif len(lineage) == 1:
				parent = lineage[0]

			else:
				if p in lineage:
					lineage.remove(p)
				parent = lineage[-1]

			level = raw_entry.get('hierarchy_level', 0)

			if parent == '' or level == 0:
				publishers[id] = {
					'id': id,
					'title': title,
					'titles': titles,
				}

			else:
				sub_publishers[id] = {
					'id': id,
					'title': title,
					'titles': titles,
					'parent': parent,
				}

			roles = get_list(raw_entry, 'roles')

			for role in roles:
				if get_string(role, 'role') == 'institution':
					institutions[clean_id(get_string(role, 'id'))] = {
						'parent': id
					}

	for sub in sub_publishers.values():
		if sub['parent'] not in publishers:
			print(f'{sub["id"]}: parent {sub["parent"]} not found')
			continue

		publishers[sub['parent']]['titles'] = remove_duplicates(
			publishers[sub['parent']]['titles'] + [sub['title']] + sub['titles']
		)

	with open(output_path, 'w', encoding='utf-8') as out_file:
		out_file.write(json.dumps(publishers) + '\n')

	return publishers, sub_publishers, institutions


def process_journals(
	publishers: dict[str, dict[str, Any]],
	sub_publishers: dict[str, dict[str, Any]],
	institutions: dict[str, dict[str, Any]],
	verbose: bool = False,
) -> dict[str, dict[str, Any]]:
	if verbose:
		print('Journals...')

	raw_path = 'data/openalex/raw/journals.jsonl'
	output_path = 'data/openalex/journals.json'

	if verbose:
		print('  Download...')

	if not os.path.exists(raw_path):
		import_raw('https://openalex.s3.amazonaws.com/data/sources', raw_path)

	if verbose:
		print('  Process...')

	if os.path.exists(output_path):
		os.remove(output_path)

	journals = {}
	publisher_rank = {}
	journal_rank = []

	with open(raw_path, 'r', encoding='utf-8') as in_file:
		for line in in_file.readlines():
			line = line.strip()

			if not line:
				continue

			raw_entry = json.loads(line)
			id = clean_id(get_string(raw_entry, 'id'))
			title = clean_text(get_string(raw_entry, 'display_name'))

			if id == '' or title == '' or get_string(raw_entry, 'type') != 'journal':
				continue

			publisher_id = clean_id(get_string(raw_entry, 'host_organization'))
			publisher = None

			if publisher_id != '':
				if publisher_id in publishers:
					publisher = publisher_id

				elif publisher_id in sub_publishers:
					publisher = sub_publishers[publisher_id]['parent']

				elif publisher_id in institutions:
					p_id = institutions[publisher_id]['parent']

					if p_id in publishers:
						publisher = p_id

					elif p_id in sub_publishers:
						publisher = sub_publishers[p_id]['parent']

				if publisher_id is None:
					print(f'{id}: publisher {publisher_id} not found')

			h = get_dict(raw_entry, 'summary_stats').get('h_index')

			if publisher is not None and h is not None:
				if publisher not in publisher_rank:
					publisher_rank[publisher] = { 'title': publishers[publisher]['title'], 'h': 0 }
				publisher_rank[publisher]['h'] += h

			if h is not None:
				journal_rank.append({ 'title': title, 'h': h })

			journals[id] = {
				'id': id,
				'issns': [clean_issn(issn) for issn in get_list(raw_entry, 'issn')],
				'title': title,
				'titles': clean_list(
					get_list(raw_entry, 'alternate_titles') +
					[raw_entry.get('abbreviated_title')]
				),
				'publisher': publisher,
				'metrics': {
					'if': get_dict(raw_entry, 'summary_stats').get('2yr_mean_citedness'),
					'h': h,
				},
				'link': raw_entry.get('homepage_url'),
			}

	with open(output_path, 'w', encoding='utf-8') as out_file:
		out_file.write(json.dumps(journals) + '\n')

	publisher_rank = sorted(publisher_rank.values(), key=lambda x: x['h'], reverse=True)
	journal_rank = sorted(journal_rank, key=lambda x: x['h'], reverse=True)

	if verbose:
		print('Publishers:')

		for publisher in publisher_rank[:10]:
			print(f'  {publisher["title"]}: {publisher["h"]:,}')

		print('Journals:')

		for journal in journal_rank[:10]:
			print(f'  {journal["title"]}: {journal["h"]:,}')

	return journals


def get_data(verbose: bool = False) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
	if os.path.exists('data/openalex/publishers.json') and os.path.exists('data/openalex/journals.json'):
		with open('data/openalex/publishers.json') as publishers_file, \
			 open('data/openalex/journals.json') as journals_file:
			publishers = json.load(publishers_file)
			journals = json.load(journals_file)
	else:
		if not os.path.exists('data/openalex/raw'):
			os.makedirs('data/openalex/raw')

		publishers, sub_publishers, institutions = process_publishers(verbose)
		journals = process_journals(publishers, sub_publishers, institutions, verbose)

	print(f'Loaded {len(journals):,} journals and {len(publishers):,} publishers')
	return publishers, journals
