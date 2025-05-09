from typing import Any
import os, json, math
from copy import deepcopy
from data.fields import *
from data.utils import *


# The metrics used to compute the scores
METRICS = [
	'h', # H-index
	'if', # Impact Factor
	'cs', # CiteScore
	'sjr', # SCImago Journal Rank
	'snip', # Source Normalized Impact per Paper
	'ef', # Eigenfactor Score
	'ai', # Article Influence Score
	'self', # Self-citation rate
	'rti', # Rigor & Transparency Index
	'top', # Transparency and Openness Promotion Factor
	'alt', # Altmetric (Average News Mentions)
]

SELF_CITATION_THRESHOLD = 0.05 # The self-citation threshold before applying a penalty
MIN_VALUES = 10 # The minimum number of values required to compute a score
NONE_PENALTY = 0.1 # The penalty for missing metrics


# Apply an exponential curve to a value between 0 and 1
def exp_curve(value: float, metric: str) -> float:
	if metric in ['rti', 'top']:
		return value

	if metric == 'oa':
		return (math.exp(6 * value) - 1) / (math.exp(6) - 1)

	return 1 - math.sqrt(1 - value ** 2)


# Compute the normalized ranking of a list of values
def compute_normalized_ranking(values: dict[str, int | float]) -> dict[str, float]:
	if len(values) == 0:
		return {}

	# Group identical values
	values_dict = {}

	for id, value in values.items():
		if value not in values_dict:
			values_dict[value] = [id]
		else:
			values_dict[value].append(id)

	rank = 0
	ranks = {id: i for i, (id, _) in enumerate(sorted(values.items(), key=lambda x: x[1]))}

	# Compute ranks
	for value in sorted(list(values_dict.keys())):
		for id in values_dict[value]:
			ranks[id] = rank
			rank += 1

		# Apply the average rank for identical values
		mean_rank = sum(ranks[id] for id in values_dict[value]) / len(values_dict[value])

		for id in values_dict[value]:
			ranks[id] = mean_rank

	# Normalize ranks
	min_rank = min(ranks.values())
	max_rank = max(ranks.values())

	if min_rank == max_rank:
		return {}

	return {id: ratio(rank, min_rank, max_rank) for id, rank in ranks.items()}


# Compute the scores of a metric
def compute_scores(metric_values: dict[str, int | float], metric: str) -> dict[str, float]:
	if len(metric_values) < MIN_VALUES:
		return {}

	# Normalize and inverted values for self-citation rate
	if metric == 'self':
		return {id: exp_curve(1.0 - ratio(value, SELF_CITATION_THRESHOLD, 1), metric) for id, value in metric_values.items()}

	ranks = compute_normalized_ranking(metric_values)

	# Exponential curve of the ranking for the other metrics
	return {id: exp_curve(rank, metric) for id, rank in ranks.items()}


# Compute and save the scores of the journals
def generate_scores() -> None:

	if os.path.exists(os.path.join('journals.json')):
		os.remove(os.path.join('journals.json'))

	# === Load the raw data === #

	with open(os.path.join('data/journals.json'), 'r', encoding='utf-8') as file:
		data = json.load(file)

	journals: dict[str, dict[str, Any]] = {journal['id']: journal for journal in data}

	# === Keep only rankable journals === #

	rankable_journals: dict[str, dict[str, Any]] = {}

	for id, journal in journals.items():
		journal_copy = deepcopy(journal)

		# Skip if no metrics
		if len(journal_copy['metrics']) == 0:
			continue

		rankable_journals[id] = journal_copy

	total_size = len(rankable_journals)
	print(f'Ranking {total_size:,} journals out of {len(journals):,}')

	# === List journal fields === #

	fields = {}

	for id, journal in rankable_journals.items():
		field_list = []

		for field in journal['fields']:
			if field == 1000:
				field_list.extend(ID_TO_FIELD.keys())
			elif ID_TO_FIELD[field] in FIELDS:
				field_list.extend([FIELD_TO_ID[f.lower()] for f in FIELDS[ID_TO_FIELD[field]]])

			field_list.append(field)

		fields[id] = list(set(field_list))

	# === Compute metric scores === #

	metric_scores: dict[str, dict[str, float]] = {id: {metric: None for metric in METRICS} for id in rankable_journals}

	for metric in METRICS:
		# Compute scores for the journals with the metric
		journal_ids = [id for id, journal in rankable_journals.items() if metric in journal['metrics']]
		scores = compute_scores({id: rankable_journals[id]['metrics'][metric] for id in journal_ids}, metric)

		for id in scores:
			metric_scores[id][metric] = scores[id]

		# Self-citation rate scores don't rely on ranking
		if metric == 'self':
			continue

		# Compute scores for each field
		field_scores: dict[str, list[float]] = {id: [] for id in rankable_journals}

		for field in ID_TO_FIELD.keys():
			field_journal_ids = [id for id in journal_ids if field in fields[id]]
			scores = compute_scores({id: rankable_journals[id]['metrics'][metric] for id in field_journal_ids}, metric)

			for id in scores:
				field_scores[id].append(scores[id])

		# Merge all field scores and merge it with the global metric score
		for id in field_scores:
			if len(field_scores[id]) > 0:
				metric_scores[id][metric] = (metric_scores[id][metric] + (sum(field_scores[id]) / len(field_scores[id]))) / 2

	# === Compute overall scores === #

	overall_scores: dict[str, float] = {}

	for id, journal in rankable_journals.items():
		score = 0.0
		total = 0.0

		# Fill nominator and denominator of the weighted average
		for metric in METRICS:
			if metric in journal['metrics']:
				score += metric_scores[id][metric]
				total += 1
			else:
				total += NONE_PENALTY

		# Compute the global score
		overall_scores[id] = score / total

	# Merge the overall scores with the exponential curve of the ranking
	overall_scores = {id: (overall_scores[id] + exp_curve(rank, 'oa')) / 2 for id, rank in compute_normalized_ranking(overall_scores).items()}

	# === Update journals data === #

	# Add scores to journals
	for id, score in overall_scores.items():
		journals[id]['scores'] = {'oa': score}

		for metric in METRICS:
			journals[id]['scores'][metric] = metric_scores[id][metric] if metric_scores[id][metric] is not None else None

	# Add missing scores
	for journal in journals.values():
		if 'scores' not in journal:
			journal['scores'] = {}

	# Sort by overall rank
	journals_list = sorted(
		list(journals.values()),
		key=lambda journal: journal['scores']['oa'] if 'oa' in journal['scores'] and journal['scores']['oa'] is not None else -1,
		reverse=True,
	)

	# To dict
	for journal in journals_list:
		journal.pop('fields', None)

	results = {journal['id']: journal for journal in journals_list}

	# === Save === #

	with open(os.path.join('journals.json'), 'w', encoding='utf-8') as file:
		json.dump(remove_none(results), file, ensure_ascii=False)
