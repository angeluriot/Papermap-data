import os
import pandas as pd
from data.utils import *
from data.fields import *


def clean_field(field: str) -> str:
	return field.lower().replace('(q1)', '').replace('(q2)', '').replace('(q3)', '').replace('(q4)', '').replace('(miscellaneous)', '').strip()


def get_data() -> list[dict[str, str | Any]]:
	journals = {}

	for path in os.listdir('data/scimago/raw'):
		if path.startswith('.') or not path.endswith('.csv'):
			continue

		year = int(''.join([c for c in path if c.isnumeric()]))

		df = pd.read_csv(
			filepath_or_buffer=f'data/scimago/raw/{path}',
			sep=';',
			dtype=str,
			keep_default_na=False,
			na_values=[],
			encoding='utf-8',
		)

		for _, row in df.iterrows():
			if str(row['Type']).lower().strip() != 'journal':
				continue

			journal = {
				'scopus_id': str(row['Sourceid']).strip(),
				'issns': remove_duplicates([clean_issn(issn) for issn in row['Issn'].split(',')]),
				'title': clean_text(row['Title']),
				'titles': [],
				'active': None,
				'in_scopus': None,
				'last_year': int(str(row['Coverage']).strip()[-4:]) if str(row['Coverage']).strip() != '' else None,
				'publisher_titles': clean_list([row['Publisher']]),
				'fields': sorted(remove_duplicates([
					FIELD_TO_ID[clean_field(field)]
					for field in row['Categories'].strip().split(';')
					if row['Categories'].strip() != ''
				])),
				'metrics': {
					'if': clean_number(str(row['Citations / Doc. (2years)'])),
					'h': clean_number(str(row['H index'])),
					'sjr': clean_number(str(row['SJR'])),
				},
			}

			id = journal['scopus_id']

			if id not in journals or year > journals[id][1]:
				journals[id] = (journal, year)

	journals = [journal for journal, _ in journals.values()]

	print(f'Loaded {len(journals):,} journals')

	return journals
