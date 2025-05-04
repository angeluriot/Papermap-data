import json
import requests
import gzip
import io

data = {}
output_path = './test_data.jsonl'
i = 0

with open(output_path, 'w', encoding='utf-8') as out_file:
	# Fetch the manifest listing all part_*.gz files
	manifest_url = 'https://openalex.s3.amazonaws.com/data/sources/manifest'
	resp = requests.get(manifest_url)
	resp.raise_for_status()
	manifest = resp.json()

	# Iterate over each entry in the manifest
	for entry in manifest.get('entries', []):
		s3_url = entry.get('url')
		# convert s3:// URL to HTTP(s) URL
		file_url = s3_url.replace('s3://openalex', 'https://openalex.s3.amazonaws.com')
		r = requests.get(file_url, stream=True)
		r.raise_for_status()

		# stream, decompress and process each line
		with gzip.GzipFile(fileobj=r.raw) as gz:
			reader = io.TextIOWrapper(gz, encoding='utf-8')
			for line in reader:
				line = line.strip()
				if not line:
					continue

				if i % 1000 == 0:
					print(f'Processed {i:,} lines', end='\r')

				obj = json.loads(line)
				out_file.write(line + '\n')
				if 'type' in obj:
					data[obj['type']] = data.get(obj['type'], 0) + 1
				i += 1

print(data)
