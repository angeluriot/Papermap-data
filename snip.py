import csv, random
from utils import *


def get_snip():

	snip_data = {}
	snip_journals = []
	snip_metrics = []

	with open('./raw/snip_csv.csv', 'r', encoding='utf-8') as f:
		snip_raw_data = csv.reader(f, delimiter=';')

		for row in snip_raw_data:

			if row[1].strip() == 'Source type':
				continue

			other = snip_data.get(row[0].strip())

			if other is None or int(row[5].strip()) > int(other[5].strip()):
				snip_data[row[0].strip()] = row

	snip_data = list(snip_data.values())

	for row in snip_data:

		title = row[0].strip().replace('&amp;', '&')
		type = JOURNAL_TYPES[row[1].strip().lower()]

		if title == '' or type == 'Conference and Proceedings' or type == 'Trade Journal':
			continue

		snip_journals.append({
			'titles': [title],
			'pissn': clean_issn(row[2]) if clean_issn(row[2]) != '' else None,
			'eissn': clean_issn(row[3]) if clean_issn(row[3]) != '' else None,
			'issns': remove_duplicates(filter(None, [clean_issn(row[2]) if clean_issn(row[2]) != '' else None, clean_issn(row[3]) if clean_issn(row[3]) != '' else None])),
			'type': type,
			'publisher': None,
			'scopes': sorted(remove_duplicates([ID_TO_SCOPE[int(scope.strip())] for scope in row[4].strip().split(';') if scope != '' and scope != 'NULL']), key = lambda x: SCOPE_TO_ID[x.lower()]),
			'sjr': None
		})
		snip_metrics.append({
			'snip_2': {
				'year': int(row[5].strip()) if row[5].strip().isnumeric() else 2023,
				'value': float(row[11].strip().replace(',', '.')) if row[11].strip().replace(',', '').isnumeric() else None
			},
			'self_1': {
				'year': int(row[5].strip()) if row[5].strip().isnumeric() else 2023,
				'value': float(row[14].strip().replace(',', '.').replace('%', '')) if row[14].strip().replace(',', '').replace('%', '').isnumeric() else None
			}
		})

	print(f'Size: {len(snip_journals):,}\n')

	for _ in range(5):
		print(snip_journals[random.randint(0, len(snip_journals) - 1)])

	for _ in range(5):
		print(snip_metrics[random.randint(0, len(snip_metrics) - 1)])

	return snip_journals, snip_metrics
