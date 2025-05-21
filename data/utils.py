from typing import Any
from bs4 import BeautifulSoup
import html
import unicodedata


def get_string(dict: dict[str, str | None], key: str) -> str:
	value = dict.get(key)
	return '' if value is None else value


def get_list(dict: dict[str, list[Any] | None], key: str) -> list[Any]:
	value = dict.get(key)
	return [] if value is None else value


def get_dict(dict: dict[str, dict[str, Any] | None], key: str) -> dict[str, Any]:
	value = dict.get(key)
	return {} if value is None else value


def clean_text(text: str) -> str:
	cleaned = html.unescape(str(text)).replace('&quot;', '"').strip()

	if '<' in cleaned and '>' in cleaned:
		parts = cleaned.split('&')
		parts = [BeautifulSoup(part, "html.parser").get_text() for part in parts]
		cleaned = '&'.join(parts).strip()

	cleaned = unicodedata.normalize('NFC', cleaned)

	for c in ['\r', '\n', '\t', '\uFEFF', '\u200B', '\u200A', '\u00A0']:
		cleaned = cleaned.replace(c, ' ')

	while '  ' in cleaned:
		cleaned = cleaned.replace('  ', ' ')

	return cleaned.strip()


def clean_issn(issn: str) -> str:
	return ''.join([c for c in str(issn) if c.isalpha() or c.isnumeric()]).upper().strip()


def remove_duplicates(list: list) -> list:
	cleaned_list = [x for x in list if x != '' and x is not None]
	seen = set()
	return [x for x in cleaned_list if not (x in seen or seen.add(x))]


def clean_list(list: list[str | None]) -> list[str]:
	return remove_duplicates([clean_text(item) for item in list if item is not None])


def clean_id(id: str | None) -> str:
	return str(id).replace('https://openalex.org/', '').upper().strip() if id is not None else ''


def over_clean_text(text: str) -> str:
	return ''.join([c for c in text.replace('&', 'and').lower().strip() if c.isalpha() or c.isnumeric()])


def clean_number(text: str) -> float | int | None:
	cleaned = text.replace(',', '.').strip()

	if not cleaned.replace('.', '').isnumeric():
		return None

	return float(cleaned) if '.' in cleaned else int(cleaned)


def n_sum(list: list[float | None]) -> float:
	return sum([x for x in list if x is not None])


def remove_none(value):
	if isinstance(value, dict):
		return {k: remove_none(v) for k, v in value.items() if v is not None}

	if isinstance(value, list):
		return [remove_none(x) for x in value if x is not None]

	return value


def ratio(value: float | int, min_value: float | int, max_value: float | int) -> float:
	return max(0.0, min(1.0, (value - min_value) / (max_value - min_value)))
