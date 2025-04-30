import json, random
from utils import *


def get_ef():

	ef_journals = []
	ef_metrics = []

	with open('./raw/ef_ai.json', 'r', encoding='utf-8') as f:
		ef_data = json.load(f)

	for row in ef_data:

		title = row[1].strip().replace('&amp;', '&')

		if title == '':
			continue

		ef_journals.append({
			'titles': [title],
			'pissn': None,
			'eissn': None,
			'issns': [clean_issn(row[0])],
			'type': None,
			'publisher': None,
			'scopes': [],
			'sjr': None
		})
		ef_metrics.append({
			'ef_1': {
				'year': 2015,
				'value': row[2] if type(row[2]) == float else None
			},
			'ai_1': {
				'year': 2015,
				'value': row[4] if type(row[4]) == float else None
			}
		})

	print(f'Size: {len(ef_journals):,}\n')

	for _ in range(5):
		print(ef_journals[random.randint(0, len(ef_journals) - 1)])

	for _ in range(5):
		print(ef_metrics[random.randint(0, len(ef_metrics) - 1)])

	return ef_journals, ef_metrics
