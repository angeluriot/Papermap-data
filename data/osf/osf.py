from typing import Any
import pandas as pd
from data.utils import *


def get_data(file: str) -> list[dict[str, str | Any]]:
	journals = []

	df = pd.read_csv(
		filepath_or_buffer=f'data/osf/raw/{file}',
		sep=',',
		dtype=str,
		keep_default_na=False,
		na_values=[],
		encoding='utf-8',
	)

	for _, row in df.iterrows():
		journals.append({
			'scopus_id': None,
			'issns': remove_duplicates([clean_issn(row['Issn']), clean_issn(row['Eissn'])]),
			'title': clean_text(row['Journal']),
			'titles': [],
			'active': None,
			'in_scopus': None,
			'last_year': None,
			'publisher_titles': clean_list([row['Publisher']]),
			'fields': [],
			'metrics': {
				'top': clean_number(str(row['Total'])),
			},
		})

	print(f'Loaded {len(journals):,} journals')

	return journals
