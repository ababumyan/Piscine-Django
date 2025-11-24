#!/usr/bin/env python3


from __future__ import annotations

import argparse
import re
import sys
from typing import Optional

import requests

WIKI_API = "https://{lang}.wikipedia.org/w/api.php"

USER_AGENT = "request_wikipedia/1.0 (https://github.com/ababumyan)"

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": USER_AGENT})


def sanitize_filename(title: str) -> str:
    s = title.strip().replace(' ', '_')
    s = re.sub(r'[^A-Za-z0-9_\-\.]', '', s)
    if not s:
        s = 'result'
    return f"{s}.wiki"


def search_best_title(query: str, lang: str = 'en') -> Optional[str]:
    """Return the best-matching page title for the query or None."""
    api = WIKI_API.format(lang=lang)
    params = {
        'action': 'query',
        'list': 'search',
        'srsearch': query,
        'srlimit': 1,
        'format': 'json',
    }
    try:
        r = SESSION.get(api, params=params, timeout=20)
        r.raise_for_status()
    except requests.HTTPError as e:
        # give a clearer message for 403 Forbidden from Wikimedia
        if getattr(e.response, 'status_code', None) == 403:
            print("Network error when querying Wikipedia: 403 Forbidden - the API may require a proper User-Agent.", file=sys.stderr)
        else:
            print(f"Network error when querying Wikipedia: {e}", file=sys.stderr)
        return None
    except requests.RequestException as e:
        print(f"Network error when querying Wikipedia: {e}", file=sys.stderr)
        return None

    data = r.json()
    search = data.get('query', {}).get('search', [])
    if search:
        return search[0].get('title')

    try:
        r2 = SESSION.get(api, params={'action': 'opensearch', 'search': query, 'limit': 1, 'format': 'json'}, timeout=10)
        r2.raise_for_status()
        op = r2.json()
        titles = op[1] if len(op) > 1 else []
        if titles:
            return titles[0]
    except requests.RequestException:
        return None

    return None


def get_extract_for_title(title: str, lang: str = 'en') -> Optional[str]:
    api = WIKI_API.format(lang=lang)
    params = {
        'action': 'query',
        'prop': 'extracts',
        'explaintext': 1,
        'exintro': 0,
        'titles': title,
        'format': 'json',
    }
    try:
        r = SESSION.get(api, params=params, timeout=10)
        r.raise_for_status()
    except requests.HTTPError as e:
        if getattr(e.response, 'status_code', None) == 403:
            print("Network error when fetching page extract: 403 Forbidden - check User-Agent.", file=sys.stderr)
        else:
            print(f"Network error when fetching page extract: {e}", file=sys.stderr)
        return None
    except requests.RequestException as e:
        print(f"Network error when fetching page extract: {e}", file=sys.stderr)
        return None

    data = r.json()
    pages = data.get('query', {}).get('pages', {})
    if not pages:
        return None

    # pages is a dict keyed by pageid
    for page in pages.values():
        extract = page.get('extract')
        if extract:
            return extract

    return None


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description='Search Wikipedia and write a plain-text result file.')
    parser.add_argument('query', nargs='?', help='Search string (required)')
    parser.add_argument('lang', nargs='?', default='en', help="Language code: 'en' or 'fr' (default 'en')")
    args = parser.parse_args(argv)

    if not args.query:
        print('Error: missing search parameter.', file=sys.stderr)
        return 1
    print(args)
    lang = args.lang.lower()
    if lang not in ('en', 'fr'):
        print("Error: language must be 'en' or 'fr'.", file=sys.stderr)
        return 1

    query = args.query.strip()
    if not query:
        print('Error: empty search parameter.', file=sys.stderr)
        return 1

    title = search_best_title(query, lang=lang)
    if not title:
        print('Error: no result found or network problem.', file=sys.stderr)
        return 1

    extract = get_extract_for_title(title, lang=lang)
    if extract is None:
        print('Error: could not retrieve page content.', file=sys.stderr)
        return 1

    # The file name must not contain spaces
    filename = sanitize_filename(query)
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            # Write a header line with the chosen article title, then the extract
            f.write(f"Title: {title}\n\n")
            f.write(extract)
    except OSError as e:
        print(f"Error writing file '{filename}': {e}", file=sys.stderr)
        return 1

    print(f"Wrote result to: {filename}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
