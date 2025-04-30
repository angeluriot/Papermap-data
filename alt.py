import csv, random
from utils import *


def get_alt():

	alt_data = []
	alt_journals = []
	alt_metrics = []

	with open('./raw/altmetrics.csv', 'r', encoding='utf-8') as f:
		alt_raw_data = csv.reader(f, delimiter=',')

		for row in alt_raw_data:

			if row[1].strip() == 'OA (%)':
				continue

			alt_data.append(row)

	for row in alt_data:

		title = row[0].strip().replace('&amp;', '&')

		if title == '':
			continue

		alt_journals.append({
			'titles': [title],
			'pissn': None,
			'eissn': None,
			'issns': [],
			'type': None,
			'publisher': None,
			'scopes': [],
			'sjr': None
		})
		alt_metrics.append({
			'alt_1': {
				'year': 2023,
				'value': float(row[5].strip()) if row[5].strip().replace('.', '').isnumeric() else None
			}
		})

	print(f'Size: {len(alt_journals):,}\n')

	for _ in range(5):
		print(alt_journals[random.randint(0, len(alt_journals) - 1)])

	for _ in range(5):
		print(alt_metrics[random.randint(0, len(alt_metrics) - 1)])

	return alt_journals, alt_metrics
