from utils import *
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


def create_pairs(journals, metrics, data):

	journal_pissns = {}
	journal_eissns = {}
	journal_issns = {}
	journal_titles = {}
	journal_sjrs = {}

	for id, journal in journals.items():

		if journal['pissn'] is not None:
			journal_pissns[journal['pissn']] = journal_pissns.get(journal['pissn'], []) + [id]

		if journal['eissn'] is not None:
			journal_eissns[journal['eissn']] = journal_eissns.get(journal['eissn'], []) + [id]

		for issn in journal['issns']:
			journal_issns[issn] = journal_issns.get(issn, []) + [id]

		titles = enrich_titles(journal['titles'])

		for title in titles:
			journal_titles[clean_text(title)] = journal_titles.get(clean_text(title), []) + [id]

		if metrics['sjr_1'].get(id) is not None:
			journal_sjrs[metrics['sjr_1'][id]['value']] = journal_sjrs.get(metrics['sjr_1'][id]['value'], []) + [id]

	row_to_journals = {}

	for i, row in enumerate(data):

		js = []

		if row['pissn'] is not None:
			js += journal_pissns.get(row['pissn'], [])

		if row['eissn'] is not None:
			js += journal_eissns.get(row['eissn'], [])

		for issn in row['issns']:
			js += journal_issns.get(issn, [])

		titles = enrich_titles(row['titles'])

		for title in titles:
			js += journal_titles.get(clean_text(title), [])

		if row['sjr'] is not None:
			js += journal_sjrs.get(row['sjr'], [])

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


def include_data(journals, metrics, data, exact_matches, pairs):

	row_to_journal = exact_matches.copy()
	journal_to_row = {j: r for r, j in exact_matches.items()}

	scores = []

	for r, j in pairs:

		points = 0

		row = data[r]
		journal = journals[j]

		if row['pissn'] is not None and journal['pissn'] is not None:
			if row['pissn'] == journal['pissn']:
				points += 10
			else:
				points -= 1

		if row['eissn'] is not None and journal['eissn'] is not None:
			if row['eissn'] == journal['eissn']:
				points += 10
			else:
				points -= 1

		points += len(set(row['issns']).intersection(set(journal['issns'])))

		points *= 100

		journal_titles = journal['titles']
		row_titles = row['titles']

		for i, title in enumerate(journal_titles):
			if title in row_titles:
				points += 10 - i

		points *= 10

		journal_titles = [clean_text(title) for title in journal['titles']]
		row_titles = [clean_text(title) for title in row['titles']]

		for i, title in enumerate(journal_titles):
			if title in row_titles:
				points += 10 - i

		points *= 10

		journal_titles = [clean_text(title) for title in enrich_titles(journal['titles'])]
		row_titles = [clean_text(title) for title in enrich_titles(row['titles'])]

		for title in enumerate(journal_titles):
			if title in row_titles:
				points += 1

		points *= 10

		if row['publisher'] is not None and clean_text(row['publisher']) in [clean_text(p) for p in journal['publishers']]:
			points += 1

		points *= 10

		if row['sjr'] is not None and metrics['sjr_1'].get(j) is not None:
			if row['sjr'] == metrics['sjr_1'][j]['value']:
				points += 1
			else:
				points -= 1

		points *= 10

		if journal['removed'] == False:
			points += 2
		elif journal['removed'] == True:
			points -= 2

		if journal['active'] == True:
			points += 1
		elif journal['active'] == False:
			points -= 1

		points *= 10

		if journal['type'] is not None and row['type'] is not None:
			if journal['type'] == row['type']:
				points += 1
			else:
				points -= 1

		points *= 10

		points += len(set(journal['scopes']).intersection(set(row['scopes'])))

		points *= 1_000

		if journal['last_year'] is not None:
			points += journal['last_year'] - 1700

		points *= 2_000

		points += metrics['h_1'].get(j, {'value': -1})['value']

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


def update_metrics(journal_metrics, data_metrics, exact_matches):

	for r, j in exact_matches.items():
		for key in data_metrics[r].keys():

			if data_metrics[r][key] is None or data_metrics[r][key]['year'] is None or data_metrics[r][key]['value'] is None:
				continue

			if key not in journal_metrics:
				journal_metrics[key] = {}

			journal_metrics[key][j] = data_metrics[r][key]

	return journal_metrics
