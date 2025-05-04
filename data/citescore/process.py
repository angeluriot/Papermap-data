import os, csv, random


def get_citescore():

	citescore_journals = []
	citescore_metrics = []
	citescore_data_set = set()

	full_size = 0
	final_size = 0

	for path in os.listdir('./raw/citescore'):
		if not path.endswith('.csv'):
			continue

		with open(os.path.join('./raw/citescore', path), 'r', encoding='utf-8') as f:
			citescore_raw_data = csv.reader(f, delimiter=';')

			for row in citescore_raw_data:

				if row[1].strip() == 'CiteScore':
					continue

				full_size += 1

				if ''.join(row) in citescore_data_set:
					continue

				title = row[0].strip().replace('&amp;', '&')

				if title == '':
					continue

				if title == 'Wine Economics and Policy' and 'Diabetes' in row[2].strip():
					title = 'The Lancet Diabetes and Endocrinology'


				citescore_data_set.add(''.join(row))
				citescore_journals.append({
					'titles': [title],
					'pissn': None,
					'eissn': None,
					'issns': [],
					'type': None,
					'publisher': row[8].strip().replace('&amp;', '&') if row[8].strip() != '' else None,
					'scopes': [],
					'sjr': float(row[7].strip().replace(',', '.')) if row[7].strip().replace(',', '').isnumeric() else None
				})
				citescore_metrics.append({
					'cs_1': {
						'year': 2023,
						'value': float(row[1].strip().replace(',', '.')) if row[1].strip().replace(',', '').isnumeric() else None
					},
					'snip_1': {
						'year': 2023,
						'value': float(row[6].strip().replace(',', '.')) if row[6].strip().replace(',', '').isnumeric() else None
					},
					'sjr_2': {
						'year': 2023,
						'value': float(row[7].strip().replace(',', '.')) if row[7].strip().replace(',', '').isnumeric() else None
					}
				})
				final_size += 1

	print(f'Full size: {full_size:,}')
	print(f'Final size: {final_size:,}\n')

	for _ in range(5):
		print(citescore_journals[random.randint(0, len(citescore_journals) - 1)])

	for _ in range(5):
		print(citescore_metrics[random.randint(0, len(citescore_metrics) - 1)])

	return citescore_journals, citescore_metrics
