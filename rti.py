import json, random


def get_rti():

	rti_journals = []
	rti_metrics = []

	with open('./raw/rti.json', 'r', encoding='utf-8') as f:
		rti_raw_data = json.load(f)

	rti_data = {}

	for row in rti_raw_data['data']:
		other = rti_data.get(row[0].strip())

		if other is None or int(row[1].strip()) > int(other[1].strip()):
			rti_data[row[0].strip()] = row

	rti_data = list(rti_data.values())

	for row in rti_data:

		title = row[0].strip().replace('&amp;', '&')

		if title == '':
			continue

		rti_journals.append({
			'titles': [title],
			'pissn': None,
			'eissn': None,
			'issns': [],
			'type': None,
			'publisher': None,
			'scopes': [],
			'sjr': None
		})
		rti_metrics.append({
			'rti_1': {
				'year': int(row[1].strip()) if row[1].strip().isnumeric() else 2020,
				'value': float(row[3].strip()) if row[1].strip().replace('.', '').isnumeric() else None
			}
		})

	print(f'Size: {len(rti_journals):,}\n')

	for _ in range(5):
		print(rti_journals[random.randint(0, len(rti_journals) - 1)])

	for _ in range(5):
		print(rti_metrics[random.randint(0, len(rti_metrics) - 1)])

	return rti_journals, rti_metrics
