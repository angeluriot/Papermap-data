from utils import *

def get_duplicates(journals: dict[str, dict[str, str | list[str] | bool, int]]) -> tuple[dict[str, list[str]], dict[str, list[str]]]:

	journal_issns = {}
	journal_titles = {}

	for journal in journals:

		for issn in journals[journal]['issns']:
			journal_issns[issn] = journal_issns.get(issn, set()).union(set([journal]))

		clean_title = clean_text(
			clean_text(journals[journal]['titles'][0]) +
			' ' +
			clean_text(journals[journal]['publishers'][0] if len(journals[journal]['publishers']) > 0 else '')
		)

		journal_titles[clean_title] = journal_titles.get(clean_title, set()).union(set([journal]))

	print_values([len(i) for i in journal_issns.values()], description=' ISSNs')
	print_values([len(t) for t in journal_titles.values()], description='Titles')

	return [group for group in list(journal_issns.values()) + list(journal_titles.values()) if len(group) > 1]


def clean_duplicates(journals: dict[str, dict[str, str | list[str] | bool, int]], metrics: dict[str, dict[str, int | float]]) -> dict[str, dict[str, str | list[str] | bool, int]]:

	duplicates = get_duplicates(journals)

	def points(journal: str) -> int:

		total = 10_000_000 if journals[journal]['removed'] == False else 0
		total = 50_000_000 if journals[journal]['removed'] is None else 0
		total += 1_000_000 if journals[journal]['active'] == True else 0
		total += 500_000 if journals[journal]['active'] is None else 0
		total += metrics['h_1'].get(journal, {'value': -1})['value'] * 500
		total += journals[journal]['last_year'] if journals[journal]['last_year'] is not None else 1_700

		return total

	for group in duplicates:

		cleaned_group = [j for j in list(group) if j in journals]

		if len(cleaned_group) < 2:
			continue

		sorted_sames = sorted(cleaned_group, key=points, reverse=True)
		to_remove = [j for j in sorted_sames[1:] if points(j) < points(sorted_sames[0])]

		for journal in to_remove:
			journals[sorted_sames[0]]['ids'].append(journal)
			journals[sorted_sames[0]]['issns'] = remove_duplicates(journals[sorted_sames[0]]['issns'] + journals[journal]['issns'])
			journals.pop(journal)

	print()
	duplicates = get_duplicates(journals)

	return journals

