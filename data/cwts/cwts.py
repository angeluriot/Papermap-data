from typing import Any
from data.utils import *
from data.fields import *
import pandas as pd


def get_data(file: str, sheet: str) -> list[dict[str, str | Any]]:
	df = pd.read_excel(
		io=f'data/cwts/raw/{file}',
		dtype=str,
		keep_default_na=False,
		na_values=[],
		sheet_name=sheet,
		engine='openpyxl',
	)

	journals = {}

	for _, row in df.iterrows():
		if str(row['Source type']).lower().strip() != 'journal':
			continue

		journal = {
			'scopus_id': None,
			'issns': remove_duplicates([clean_issn(row['Print ISSN']), clean_issn(row['Electronic ISSN'])]),
			'title': clean_text(row['Source title']),
			'titles': [],
			'active': None,
			'in_scopus': None,
			'last_year': None,
			'publisher_titles': [],
			'fields': sorted(remove_duplicates([
				FIELD_TO_ID[ID_TO_FIELD[int(field.strip())].lower()]
				for field in str(row['ASJC field IDs']).strip().split(';')
				if field.strip() != '' and field.strip() != 'NULL'
			])),
			'metrics': {
				'snip': clean_number(str(row['SNIP'])),
				'self': clean_number(str(row['% self cit'])),
			},
		}

		id = journal['title'] + ''.join(journal['issns']) + ''.join([str(f) for f in journal['fields']])

		if id not in journals or int(str(row['Year']).strip()) > journals[id][1]:
			journals[id] = (journal, int(str(row['Year']).strip()))

	journals = [journal for journal, _ in journals.values()]

	print(f'Loaded {len(journals):,} journals')

	return journals
