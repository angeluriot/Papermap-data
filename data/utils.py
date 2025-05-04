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
	cleaned = html.unescape(text).replace('&quot;', '"').strip()

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
	return ''.join([c for c in issn if c.isalpha() or c.isnumeric()]).upper().strip()


def remove_duplicates(lst: list) -> list:
	cleaned_lst = [x for x in lst if x != '' and x is not None]
	seen = set()
	return [x for x in cleaned_lst if not (x in seen or seen.add(x))]


def clean_list(list: list[str | None]) -> list[str]:
	cleaned = [clean_text(item) for item in list if item is not None]
	return remove_duplicates([item for item in cleaned if item != ''])


def clean_id(id: str | None) -> str:
	return id.replace('https://openalex.org/', '').upper().strip() if id is not None else ''
