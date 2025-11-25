#!/usr/bin/env python3

import sys
import requests
from bs4 import BeautifulSoup

WIKIPEDIA_URL = "https://en.wikipedia.org"
PHILOSOPHY_URL = "https://en.wikipedia.org/wiki/Philosophy"

USER_AGENT = "request_wikipedia/1.0 "

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": USER_AGENT})

visited = []


class RoadsToPhilosophy:
    def __init__(self, start_page: str):
        self.start_page = start_page
        self.wiki = WIKIPEDIA_URL

    def fetch_page(self, page: str) -> str:
        url = self.wiki + page
        try:
            response = SESSION.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            # print(f"Error fetching {url}: {e}")
            return ""

    def run(self, page=None):
        if page is None:
            page ="/wiki/" + self.start_page
            print(f"Starting from: {page}")

        url = self.wiki + page
        # print(f"page: {url} self.wiki: {self.wiki} page: {page}")
        try:
            response = self.fetch_page(page)
            # print(f"Visiting: {url} with status code {response.status_code}")
        except requests.RequestException as e:
            # print(f"Error fetching {url}: {e}")
            return print("It leads to a dead end!")

        soup = BeautifulSoup(response, 'html.parser')

        title = soup.find(id='firstHeading')
        if not title:
            return print("It leads to a dead end!")
        title = title.text.strip()

        if title in visited:
            return print("It leads to an infinite loop!")

        visited.append(title)
        print(f" ---------------- Visiting: {title} --------------- ")

        if title == 'Philosophy':
            return print(f"{len(visited)} roads from {visited[0]} to Philosophy")

        content = soup.find(id='mw-content-text')
        if not content:
            return print("It leads to a dead end!")

        links = content.select('p > a')

        for link in links:
            href = link.get('href', '')
            if href.startswith('/wiki/') and not (href.startswith('/wiki/Wikipedia:') or href.startswith('/wiki/Help:')):
                return self.run(href)





if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 roads_to_philosophy.py <search term>")
        sys.exit(1)
    RoadsToPhilosophy(sys.argv[1]).run()


