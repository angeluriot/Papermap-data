import os, csv
from utils import *

def get_journals():
	with open('./raw/journals_cleaned.csv', 'r', encoding='utf-8') as f:
		journals_data = f.read().splitlines()

	scopus = 0
	scimago = 0
	both = 0
	journals = {}

	for journal_data in journals_data:

		data = journal_data.split('°')

		type = JOURNAL_TYPES[data[7].strip().lower()]

		if type == 'Conference and Proceedings' or type == 'Trade Journal':
			continue

		journals[data[0].strip()] = {
			'ids': [data[0].strip()],
			'titles': remove_duplicates([title.replace('&amp;', '&') for title in [data[1].strip(), data[8].strip(), data[9].strip(), data[10].strip(), data[11].strip()] if title != '']),
			'pissn': clean_issn(data[2]) if clean_issn(data[2]) != '' else None,
			'eissn': clean_issn(data[3]) if clean_issn(data[3]) != '' else None,
			'issns': remove_duplicates(list(filter(None, [clean_issn(data[2]) if clean_issn(data[2]) != '' else None, clean_issn(data[3]) if clean_issn(data[3]) != '' else None]))),
			'active': True if data[4].strip() == 'Active' else False if data[4].strip() == 'Inactive' else None,
			'last_year': int(data[5].strip()[-4:]) if data[5].strip() != '' else None,
			'removed': data[6].strip() != '',
			'type': type,
			'publishers': remove_duplicates([p for p in [data[12].strip().replace('&amp;', '&'), data[13].strip().replace('&amp;', '&')] if p != '']),
			'scopes': sorted(remove_duplicates([ID_TO_SCOPE[int(scope.strip())] for scope in data[14].strip().split(';') if scope != '']), key = lambda x: SCOPE_TO_ID[x.lower()])
		}

	metrics = {
		'if_1': {},
		'h_1': {},
		'sjr_1': {}
	}

	seen = set()

	for date in reversed(range(1999, 2024)):

		with open(os.path.join('./raw/sjr', f'{date}.csv'), 'r', encoding='utf-8') as f:

			sjr_data = csv.reader(f, delimiter=';')

			for row in sjr_data:

				if row[0].strip() == 'Rank':
					continue

				id = row[1].strip()

				if id in seen:
					continue

				seen.add(id)

				title = row[2].strip().replace('&amp;', '&') if row[2].strip() != '' else None
				issns = remove_duplicates([clean_issn(issn) for issn in row[4].strip().split(',') if clean_issn(issn) != ''])
				last_year = int(row[21].strip()[-4:]) if row[21].strip() != '' else None
				type = JOURNAL_TYPES[row[3].strip().lower()]
				publisher = row[20].strip().replace('&amp;', '&') if row[20].strip() != '' else None
				scopes = sorted(remove_duplicates([ID_TO_SCOPE[SCOPE_TO_ID[clean_scope(s)]] for s in row[22].strip().split(';') if s.strip() != '']), key = lambda x: SCOPE_TO_ID[x.lower()])

				if type == 'Conference and Proceedings' or type == 'Trade Journal':
					continue

				for s in scopes:
					assert s.lower() in SCOPE_TO_ID

				if id not in journals:

					scimago += 1

					journals[id] = {
						'ids': [id],
						'titles': [title] if title is not None else [],
						'pissn': None,
						'eissn': None,
						'issns': issns,
						'active': None,
						'last_year': last_year,
						'removed': None,
						'type': type,
						'publishers': [publisher] if publisher is not None else [],
						'scopes': scopes
					}

					for s in journals[id]['scopes']:
						assert s.lower() in SCOPE_TO_ID

				else:

					both += 1

					for issn in issns:
						if issn not in journals[id]['issns']:
							journals[id]['issns'].append(issn)

					if title is not None and title not in journals[id]['titles']:
						journals[id]['titles'].append(title)

					if last_year is not None and (journals[id]['last_year'] is None or last_year > journals[id]['last_year']):
						journals[id]['last_year'] = last_year

					if type != journals[id]['type'] and journals[id]['type'] == 'Journal':
						journals[id]['type'] = type

					if publisher is not None and publisher not in journals[id]['publishers']:
						journals[id]['publishers'].append(publisher)

					for s in scopes:
						if s not in journals[id]['scopes']:
							journals[id]['scopes'].append(s)

					journals[id]['scopes'] = sorted(journals[id]['scopes'], key = lambda x: SCOPE_TO_ID[x.lower()])

				if row[13].strip() != '':
					metrics['if_1'][id] = {
						'year': date,
						'value': float(row[13].strip().replace(',', '.')),
					}

				if row[7].strip() != '':
					metrics['h_1'][id] = {
						'year': date,
						'value': int(row[7].strip()),
					}

				if row[5].strip() != '':
					metrics['sjr_1'][id] = {
						'year': date,
						'value': float(row[5].strip().replace(',', '.')),
					}

	journals['21100237403']['titles'] = ['The Lancet Diabetes and Endocrinology', 'Lancet Diabetes and Endocrinology,The']

	publishers = {}

	for journal in journals:
		if len(journals[journal]['titles']) == 0:
			journals.pop(journal)
			continue

		for publisher in journals[journal]['publishers']:
			publishers[clean_text(publisher)] = publishers.get(clean_text(publisher), 0) + 1

	for journal in journals:

		if len(journals[journal]['publishers']) == 0:
			continue

		p = journals[journal]['publishers']
		p.sort(key = lambda x: publishers[clean_text(x)] * 10_000 - len(clean_text(x)), reverse = True)
		journals[journal]['publishers'] = p

	scopus = len(journals) - scimago - both

	print(f'{len(journals):,} journals ({both:,} from both, {scopus:,} from Scopus, {scimago:,} from Scimago)')

	return journals, metrics
