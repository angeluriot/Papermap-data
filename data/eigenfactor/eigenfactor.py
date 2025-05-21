from typing import Any
import os, json, requests
from bs4 import BeautifulSoup
import time
from data.utils import *


def import_raw(output_path :str):
	base_url = 'http://www.eigenfactor.org/projects/journalRank/rankings.php?bsearch=2015&searchby=year&orderby=efn'
	start_page = 1
	end_page = 229

	if os.path.exists(output_path):
		return

	with open(output_path, 'w', encoding='utf-8') as out_file:
		for page in range(start_page, end_page + 1):
			url = f'{base_url}&page={page}'
			response = requests.get(url)

			if response.status_code != 200:
				print(f'Failed to fetch page {page}: {response.status_code}')
				continue

			soup = BeautifulSoup(response.content, 'html.parser')
			results = soup.find_all('div', class_='results')

			for result in results:
				try:
					rank_text = result.find('div', class_='rank').text.strip()

					if not rank_text.isdigit():
						continue

					title_element = result.find('div', class_='journal')

					if title_element:
						title = title_element.contents[0].strip()
					else:
						continue

					ef_text = result.find('div', class_='EF').text.strip()
					ef = float(ef_text) if '<' not in ef_text else float(ef_text.replace('<', '')) / 2.0

					ef_percentile = int(result.find('div', class_='pholder1').find('div', class_='pnum1').text.strip())
					ai_percentile = int(result.find('div', class_='pholder2').find('div', class_='pnum2').text.strip())

					ai_elements = result.find_all('div', class_='AI')
					ai_text = ai_elements[0].text.strip()
					ai = float(ai_text) if '<' not in ai_text else float(ai_text.replace('<', '')) / 2.0
					efn_text = ai_elements[1].text.strip()
					efn = float(efn_text) if '<' not in efn_text else float(efn_text.replace('<', '')) / 2.0

					href_element = result.find_previous('h3').find('a')
					href = href_element['href'] if href_element else ''

					if href != '':
						issn = href[5:].replace('-', '')

					out_file.write(json.dumps({
						'issn': issn,
						'title': title,
						'ef': ef,
						'ef_p': ef_percentile,
						'ai': ai,
						'ai_p': ai_percentile,
						'efn': efn,
					}, ensure_ascii=False) + '\n')

				except Exception as e:
					print(f'Error parsing journal data: {e}')
					continue

			time.sleep(1)


def get_data() -> list[dict[str, Any]]:
	raw_path = 'data/eigenfactor/raw/journals.jsonl'
	journals = []

	import_raw(raw_path)

	with open(raw_path, 'r', encoding='utf-8') as in_file:
		for line in in_file.readlines():
			line = line.strip()

			if not line:
				continue

			row = json.loads(line)

			journals.append({
				'scopus_id': None,
				'issns': [clean_issn(row['issn'])],
				'title': clean_text(row['title']),
				'titles': [],
				'active': None,
				'in_scopus': None,
				'last_year': None,
				'publisher_titles': [],
				'fields': [],
				'metrics': {
					'ef': clean_number(str(row['ef'])),
					'ai': clean_number(str(row['ai'])),
				},
			})

	print(f'Loaded {len(journals):,} journals')

	return journals
