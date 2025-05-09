from typing import Any
import os, json, requests
from data.utils import *


def import_raw(output_path :str):
	url = 'https://sciscore.com/rti/server_processing.php'

	if os.path.exists(output_path):
		return

	with open(output_path, 'w', encoding='utf-8') as out_file:
		response = requests.get(url)

		if response.status_code != 200:
			print(f'Failed to fetch page {url}')
			return

		json.dump(json.loads(response.text, ensure_ascii=False), out_file)


def get_data() -> list[dict[str, Any]]:
	raw_path = 'data/sciscore/raw/journals.jsonl'
	journals = {}

	import_raw(raw_path)

	with open(raw_path, 'r', encoding='utf-8') as in_file:
		data = json.load(in_file)

		for row in data['data']:
			journal = {
				'scopus_id': None,
				'issns': [],
				'title': clean_text(row[0]),
				'titles': [],
				'active': None,
				'in_scopus': None,
				'last_year': None,
				'publisher_titles': [],
				'fields': [],
				'metrics': {
					'rti': clean_number(str(row[3])),
				},
			}

			id = journal['title']
			year = int(str(row[1]).strip())

			if id not in journals or year > journals[id][1]:
				journals[id] = (journal, year)

	journals = [journal for journal, _ in journals.values()]

	print(f'Loaded {len(journals):,} journals')

	return journals
