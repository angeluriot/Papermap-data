import csv, random
from utils import *


def get_top():

	top_data = []
	top_journals = []
	top_metrics = []

	with open('./raw/top.csv', 'r', encoding='utf-8') as f:
		top_raw_data = csv.reader(f, delimiter=',')

		for row in top_raw_data:

			if row[1].strip() == 'Issn':
				continue

			top_data.append(row)

	for row in top_data:

		title = row[0].strip().replace('&amp;', '&')

		if title == '':
			continue

		top_journals.append({
			'titles': [title],
			'pissn': clean_issn(row[1]) if clean_issn(row[1]) != '' else None,
			'eissn': clean_issn(row[2]) if clean_issn(row[2]) != '' else None,
			'issns': remove_duplicates(filter(None, [clean_issn(row[1]) if clean_issn(row[1]) != '' else None, clean_issn(row[2]) if clean_issn(row[2]) != '' else None])),
			'type': None,
			'publisher': row[4].strip() if row[4].strip() != '' else None,
			'scopes': [],
			'sjr': None
		})
		top_metrics.append({
			'top_1': {
				'year': 2023,
				'value': int(row[27].strip()) if row[27].strip().isnumeric() else None
			}
		})

	print(f'Size: {len(top_journals):,}\n')

	for _ in range(5):
		print(top_journals[random.randint(0, len(top_journals) - 1)])

	for _ in range(5):
		print(top_metrics[random.randint(0, len(top_metrics) - 1)])

	return top_journals, top_metrics
