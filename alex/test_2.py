import json

data = []
data_path = './test_data.jsonl'

with open(data_path, 'r', encoding='utf-8') as data_file:
	for line in data_file:
		line = line.strip()
		if not line:
			continue

		obj = json.loads(line)
		ratio = 0.0

		if 'topic_share' in obj:
			for topic in obj['topic_share']:
				ratio += topic['value']

		data.append(ratio)

print(sum(data) / len(data))
