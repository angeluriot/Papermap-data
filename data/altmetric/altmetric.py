from typing import Any
import pandas as pd
from data.utils import *


def get_data(file: str) -> list[dict[str, str | Any]]:
	journals = []

	df = pd.read_csv(
		filepath_or_buffer=f'data/altmetric/raw/{file}',
		sep=',',
		dtype=str,
		keep_default_na=False,
		na_values=[],
		encoding='utf-8',
	)

	for _, row in df.iterrows():
		journals.append({
			'scopus_id': None,
			'issns': [],
			'title': clean_text(row['Journal']),
			'titles': [],
			'active': None,
			'in_scopus': None,
			'last_year': None,
			'publisher_titles': [],
			'fields': [],
			'metrics': {
				'alt': clean_number(str(row['Average News Mentions'])),
			},
		})

	print(f'Loaded {len(journals):,} journals')

	return journals
