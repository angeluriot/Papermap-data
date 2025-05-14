from copy import deepcopy
from data.utils import *
import numpy as np


def enrich_titles(titles):
	new_titles = []

	for title in titles:

		if ' ' in title:
			start = title[:title.find(' ')].strip()

			if len(start) > 1 and start.isupper():
				new_titles.append(start)
				new_titles.append(title[title.find(' '):].strip())

		if title[-1] == ')' and '(' in title:
			new_titles.append(title[:title.rfind('(')].strip())

		if title.lower().startswith('world j'):
			new_titles.append('J' + title[7:].strip())

		if ' : ' in title:
			new_titles.append(title[:title.find(' : ')].strip())

		if title.lower().startswith('international j'):
			new_titles.append('J' + title[15:].strip())

		if title.lower().startswith('the '):
			new_titles.append(title[4:].strip())

		if title.lower().startswith('journal of '):
			new_titles.append((title[11].upper() + title[12:]).strip())

		if title.lower().endswith('journal'):
			new_titles.append(title[:-7].strip())

	return remove_duplicates(titles + new_titles)


def create_pairs(
	journals: dict[str, dict[str, Any]],
	data: list[dict[str, Any]]
) -> tuple[dict[int, str], list[tuple[int, str]]]:

	journal_scopus_ids = {}
	journal_issns = {}
	journal_titles = {}

	for id, journal in journals.items():
		if journal['scopus_id'] is not None:
			journal_scopus_ids[journal['scopus_id']] = journal_scopus_ids.get(journal['scopus_id'], []) + [id]

		for issn in journal['issns']:
			journal_issns[issn] = journal_issns.get(issn, []) + [id]

		titles = enrich_titles([journal['title']] + journal['titles'])

		for title in titles:
			cleaned = over_clean_text(title)
			journal_titles[cleaned] = journal_titles.get(cleaned, []) + [id]

	row_to_journals = {}

	for i, row in enumerate(data):
		js = []

		if row['scopus_id'] is not None:
			js += journal_scopus_ids.get(row['scopus_id'], [])

		for issn in row['issns']:
			js += journal_issns.get(issn, [])

		titles = enrich_titles([row['title']] + row['titles'])

		for title in titles:
			js += journal_titles.get(over_clean_text(title), [])

		js = list(set(js))

		if len(js) > 0:
			row_to_journals[i] = js

	journal_to_rows = {}

	for i, js in row_to_journals.items():
		for journal in js:
			journal_to_rows[journal] = journal_to_rows.get(journal, []) + [i]

	exact_matches = {r: js[0] for r, js in row_to_journals.items() if len(js) == 1 and len(journal_to_rows[js[0]]) == 1}
	one_journal_to_n_rows = {j: rs for j, rs in journal_to_rows.items() if len(rs) > 1}
	one_row_to_n_journals = {r: js for r, js in row_to_journals.items() if len(js) > 1}
	pairs = []

	for j, rs in one_journal_to_n_rows.items():
		for r in rs:
			pairs.append((r, j))

	for r, js in one_row_to_n_journals.items():
		for j in js:
			pairs.append((r, j))

	pairs = list(set(pairs))

	print(f'No matches: {len([i for i in range(len(data)) if i not in row_to_journals]):,}')
	print(f'Exact matches: {len(exact_matches):,}')
	print(f'1 journal to N rows: {len(one_journal_to_n_rows):,} (mean N: {np.mean([len(rs) for rs in one_journal_to_n_rows.values()]):.1f})')
	print(f'1 row to N journals: {len(one_row_to_n_journals):,} (mean N: {np.mean([len(js) for js in one_row_to_n_journals.values()]):.1f})')
	print(f'Pairs: {len(pairs):,}')

	return exact_matches, pairs


def filter_pairs(
	publishers: dict[str, dict[str, Any]],
	journals: dict[str, dict[str, Any]],
	data: list[dict[str, Any]],
	exact_matches: dict[int, str],
	pairs: list[tuple[int, str]]
) -> dict[int, str]:

	row_to_journal = exact_matches.copy()
	journal_to_row = {j: r for r, j in exact_matches.items()}
	scores = []

	for r, j in pairs:
		row = data[r]
		journal = journals[j]
		points = 1

		if row['scopus_id'] is not None and row['scopus_id'] == journal['scopus_id']:
			points += 1

		points *= 10

		points += min(9, len(set(row['issns']).intersection(set(journal['issns']))))
		points *= 10

		if row['title'] != '' and row['title'] == journal['title']:
			points += 1

		points *= 10

		if over_clean_text(row['title']) != '' and over_clean_text(row['title']) == over_clean_text(journal['title']):
			points += 1

		points *= 10
		row_titles = remove_duplicates([over_clean_text(title) for title in ([row['title']] + row['titles'])])
		journal_titles = remove_duplicates([over_clean_text(title) for title in ([journal['title']] + journal['titles'])])
		points += min(9, len(set(row_titles).intersection(set(journal_titles))))
		points *= 10
		publisher = publishers.get(journal['publisher'])

		if len(row['publisher_titles']) > 0 and publisher is not None and row['publisher_titles'][0] == publisher['title']:
			points += 1

		points *= 10

		if publisher is not None:
			row_publishers = remove_duplicates([over_clean_text(p) for p in row['publisher_titles']])
			journal_publishers = remove_duplicates([over_clean_text(p) for p in ([publisher['title']] + publisher['titles'])])
			points += min(9, len(set(row_publishers).intersection(set(journal_publishers))))

		points *= 10

		if row['active']:
			points += 1

		if journal['active']:
			points += 1

		if row['in_scopus']:
			points += 1

		if journal['in_scopus']:
			points += 1

		points *= 10
		points += min(9, len(set(journal['fields']).intersection(set(row['fields']))))
		points *= 1_000

		if row['last_year'] is not None:
			points += min(499, row['last_year'] - 1700)

		if journal['last_year'] is not None:
			points += min(499, journal['last_year'] - 1700)

		points *= 4_000
		points += min(1_999, row['metrics'].get('h', 0))
		points += min(1_999, round(np.mean(journal['metrics'].get('h', []))) if len(journal['metrics'].get('h', [])) > 0 else 0)

		scores.append((r, j, points))

	scores.sort(key = lambda x: x[2], reverse = True)
	pairs = [(r, j) for r, j, _ in scores]

	for r, j in pairs:
		if r in row_to_journal or j in journal_to_row:
			continue

		row_to_journal[r] = j
		journal_to_row[j] = r

	print(f'Included: {len(row_to_journal):,}')
	print(f'Not included: {len(data) - len(row_to_journal):,}')

	return row_to_journal


def update(
	publishers: dict[str, dict[str, Any]],
	journals: dict[str, dict[str, Any]],
	data: list[dict[str, Any]],
	exact_matches: dict[int, str],
) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:

	journals_updated = 0
	publishers_updated = set()

	for r, j in exact_matches.items():

		row = data[r]
		journal = journals[j]
		journal_copy = deepcopy(journal)
		publisher = publishers.get(journal['publisher'])
		publisher_copy = deepcopy(publisher)

		if journal['scopus_id'] is None:
			journal['scopus_id'] = row['scopus_id']

		journal['issns'] = remove_duplicates(journal['issns'] + row['issns'])
		journal['titles'] = remove_duplicates(journal['titles'] + [row['title']] + row['titles'])

		if journal['active'] is None:
			journal['active'] = row['active']

		if journal['in_scopus'] is None:
			journal['in_scopus'] = row['in_scopus']

		if journal['last_year'] is None:
			journal['last_year'] = row['last_year']

		if publisher is not None:
			publisher['titles'] = remove_duplicates(publisher['titles'] + row['publisher_titles'])

		journal['fields'] = remove_duplicates(journal['fields'] + row['fields'])

		for key, value in row['metrics'].items():
			if key not in journal['metrics']:
				journal['metrics'][key] = []

			if value is not None:
				journal['metrics'][key].append(value)

		if journal != journal_copy:
			journals_updated += 1

		if publisher is not None and publisher != publisher_copy:
			publishers_updated.add(publisher['id'])

	print(f'{journals_updated:,} ({(journals_updated / len(journals)) * 100:.2f} %) journals updated')
	print(f'{len(publishers_updated):,} ({(len(publishers_updated) / len(publishers)) * 100:.2f} %) publishers updated')

	return publishers, journals
