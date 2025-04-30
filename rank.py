def merge_metrics(journals, metrics):

	metrics['if'] = {}
	metrics['h'] = {}
	metrics['sjr'] = {}
	metrics['cs'] = {}
	metrics['rti'] = {}
	metrics['ef'] = {}
	metrics['ai'] = {}
	metrics['snip'] = {}
	metrics['self'] = {}
	metrics['top'] = {}
	metrics['alt'] = {}

	for journal in journals:
		if journal in metrics['if_1']:
			metrics['if'][journal] = metrics['if_1'][journal]

		if journal in metrics['h_1']:
			metrics['h'][journal] = metrics['h_1'][journal]

		if journal in metrics['sjr_1'] and journal not in metrics['sjr_2']:
			metrics['sjr'][journal] = metrics['sjr_1'][journal]

		if journal in metrics['sjr_2'] and journal not in metrics['sjr_1']:
			metrics['sjr'][journal] = metrics['sjr_2'][journal]

		if journal in metrics['sjr_1'] and journal in metrics['sjr_2']:
			metrics['sjr'][journal] = {
				'year': max(metrics['sjr_1'][journal]['year'], metrics['sjr_2'][journal]['year']),
				'value': (metrics['sjr_1'][journal]['value'] + metrics['sjr_2'][journal]['value']) / 2
			}

		if journal in metrics['cs_1']:
			metrics['cs'][journal] = metrics['cs_1'][journal]

		if journal in metrics['rti_1']:
			metrics['rti'][journal] = metrics['rti_1'][journal]

		if journal in metrics['ef_1']:
			metrics['ef'][journal] = metrics['ef_1'][journal]

		if journal in metrics['ai_1']:
			metrics['ai'][journal] = metrics['ai_1'][journal]

		if journal in metrics['snip_1'] and journal not in metrics['snip_2']:
			metrics['snip'][journal] = metrics['snip_1'][journal]

		if journal in metrics['snip_2'] and journal not in metrics['snip_1']:
			metrics['snip'][journal] = metrics['snip_2'][journal]

		if journal in metrics['snip_1'] and journal in metrics['snip_2']:
			metrics['snip'][journal] = {
				'year': max(metrics['snip_1'][journal]['year'], metrics['snip_2'][journal]['year']),
				'value': (metrics['snip_1'][journal]['value'] + metrics['snip_2'][journal]['value']) / 2
			}

		if journal in metrics['self_1']:
			metrics['self'][journal] = metrics['self_1'][journal]

		if journal in metrics['top_1']:
			metrics['top'][journal] = metrics['top_1'][journal]

		if journal in metrics['alt_1']:
			metrics['alt'][journal] = metrics['alt_1'][journal]

	_ = metrics.pop('if_1')
	_ = metrics.pop('h_1')
	_ = metrics.pop('sjr_1')
	_ = metrics.pop('sjr_2')
	_ = metrics.pop('cs_1')
	_ = metrics.pop('rti_1')
	_ = metrics.pop('ef_1')
	_ = metrics.pop('ai_1')
	_ = metrics.pop('snip_1')
	_ = metrics.pop('snip_2')
	_ = metrics.pop('self_1')
	_ = metrics.pop('top_1')
	_ = metrics.pop('alt_1')

	return metrics


def init_variables(journals, metrics):

	journal_metrics = {}
	journal_ranks = {}
	journal_rank_scores = {}
	overall_scores = {}
	metrics_types = ['if', 'h', 'sjr', 'cs', 'rti', 'ef', 'ai', 'snip', 'top', 'alt']

	for journal in journals:

		temp = {'journal': journal}

		for metric_type in metrics_types:
			temp[metric_type] = metrics[metric_type].get(journal, {'value': None})['value']

		journal_metrics[journal] = temp

		temp = {}

		for metric_type in metrics_types:
			temp[metric_type] = None

		journal_ranks[journal] = temp
		journal_rank_scores[journal] = temp.copy()
		overall_scores[journal] = 0.0

	return journal_metrics, journal_ranks, journal_rank_scores, overall_scores, metrics_types


def update_overall_scores(journals, journal_rank_scores, metrics_types, none_penalty = 0.1):

	overall_scores = {}

	for journal in journals:

		score = 0
		total = 0

		for metric_type in metrics_types:
			if journal_rank_scores[journal][metric_type] is not None:
				score += journal_rank_scores[journal][metric_type]
				total += 1
			else:
				total += none_penalty

		overall_scores[journal] = score / total

	return overall_scores


def update_scores(journal_metrics, journal_ranks, journal_rank_scores, overall_scores, metrics_types):

	for metric_type in metrics_types:

		js = [x for x in journal_metrics.values() if x[metric_type] is not None]
		js.sort(key=lambda x: x[metric_type] * 1_000 + overall_scores[x['journal']] * 0.001, reverse=True)

		for i, journal in enumerate(js):
			journal_ranks[journal['journal']][metric_type] = i + 1
			journal_rank_scores[journal['journal']][metric_type] = (len(js) - 1 - i) / (len(js) - 1)

	return journal_ranks, journal_rank_scores


def get_ranking(journals, metrics):

	journal_metrics, journal_ranks, journal_rank_scores, overall_scores, metrics_types = init_variables(journals, metrics)
	final_overall_scores = {}
	i = 0

	while overall_scores != final_overall_scores:
		journal_ranks, journal_rank_scores = update_scores(journal_metrics, journal_ranks, journal_rank_scores, overall_scores, metrics_types)
		final_overall_scores = overall_scores.copy()
		overall_scores = update_overall_scores(journals, journal_rank_scores, metrics_types)
		i += 1

	print(f'Converged after {i:,} iterations')

	return journal_ranks, journal_rank_scores, overall_scores
