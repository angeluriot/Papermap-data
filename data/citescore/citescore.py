import os, warnings
import pandas as pd
from data.utils import *


def get_data() -> list[dict[str, str | Any]]:
	journals = {}

	for path in os.listdir('data/citescore/raw'):
		if path.startswith('.') or not path.endswith('.xlsx'):
			continue

		with warnings.catch_warnings():
			warnings.simplefilter("ignore")

			df = pd.read_excel(
				io=f'data/citescore/raw/{path}',
				dtype=str,
				keep_default_na=False,
				na_values=[],
				sheet_name='Sheet0',
				engine='openpyxl',
			)

		for _, row in df.iterrows():
			title = clean_text(row['Source title'])

			if title == 'Wine Economics and Policy' and 'Diabetes' in row['Highest percentile']:
				title = 'The Lancet Diabetes and Endocrinology'

			journal = {
				'scopus_id': None,
				'issns': [],
				'title': title,
				'titles': [],
				'active': None,
				'in_scopus': None,
				'last_year': None,
				'publisher_titles': clean_list([row['Publisher']]),
				'fields': [],
				'metrics': {
					'cs': clean_number(str(row['CiteScore'])),
					'snip': clean_number(str(row['SNIP'])),
					'sjr': clean_number(str(row['SJR'])),
				},
			}

			id = journal['title'] + journal['publisher_titles'][0] if len(journal['publisher_titles']) > 0 else ''

			if id not in journals or (
				n_sum([journal['metrics']['cs'], journal['metrics']['snip'], journal['metrics']['sjr']])
				> n_sum([journals[id]['metrics']['cs'], journals[id]['metrics']['snip'], journals[id]['metrics']['sjr']])
			):
				journals[id] = journal

	journals = list(journals.values())

	print(f'Loaded {len(journals):,} journals')

	return journals
