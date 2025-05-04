import os, csv
from data.utils import *
from data.fields import *

def get_data():
	with open('./raw/journals_cleaned.csv', 'r', encoding='utf-8') as f:
		journals_data = f.read().splitlines()

	journals = {}

	for journal_data in journals_data:

		data = journal_data.split('°')

		if data[7].lower().strip() != 'journal':
			continue

		journals[data[0].strip()] = {
			'scopus_id': data[0].strip(),
			'titles': clean_list([data[1], data[8], data[9], data[10], data[11]]),
			'issns': remove_duplicates([clean_issn(data[2]), clean_issn(data[3])]),
			'active': data[4].strip() == 'Active' and data[6].strip() != '',
			'last_year': int(data[5].strip()[-4:]) if data[5].strip() != '' else None,
			'publisher_titles': clean_list([data[12], data[13]]),
			'fields': sorted(remove_duplicates([FIELD_TO_ID[ID_TO_FIELD[int(field.strip())]] for field in data[14].strip().split(';') if field != ''])),
		}
