from typing import Any
from data.utils import *
from data.fields import *
import pandas as pd


def get_data(file: str, sheet: str) -> list[dict[str, str | Any]]:
	df = pd.read_excel(
		io=f'data/scopus/raw/{file}',
		dtype=str,
		keep_default_na=False,
		na_values=[],
		sheet_name=sheet,
		engine='openpyxl',
	)

	journals = []

	for _, row in df.iterrows():
		if str(row['Source Type']).lower().strip() != 'journal':
			continue

		journals.append({
			'scopus_id': str(row['Sourcerecord ID']).strip(),
			'issns': remove_duplicates([clean_issn(row['ISSN']), clean_issn(row['EISSN'])]),
			'title': clean_text(row['Source Title']),
			'titles': clean_list([row['Related Title 1'], row['Other Related Title 2'], row['Other Related Title 3'], row['Other Related Title 4']]),
			'active': str(row['Active or Inactive']).strip() == 'Active',
			'in_scopus': str(row['Titles Discontinued by Scopus Due to Quality Issues']).strip() == '',
			'last_year': int(str(row['Coverage']).strip()[-4:]) if str(row['Coverage']).strip() != '' else None,
			'publisher_titles': clean_list([row['Publisher Imprints Grouped to Main Publisher'], row['Publisher']]),
			'fields': sorted(remove_duplicates([
				FIELD_TO_ID[ID_TO_FIELD[int(field.strip())].lower()]
				for field in str(row['All Science Journal Classification Codes (ASJC)']).strip().split(';') if field.strip() != ''
			])),
			'metrics': {},
		})

	print(f'Loaded {len(journals):,} journals')

	return journals
