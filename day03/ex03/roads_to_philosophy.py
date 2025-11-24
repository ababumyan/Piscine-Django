#!/usr/bin/env python3

import sys
import requests
from bs4 import BeautifulSoup

WIKIPEDIA_URL = "https://en.wikipedia.org/wiki/"
PHILOSOPHY_URL = "https://en.wikipedia.org/wiki/Philosophy"

USER_AGENT = "request_wikipedia/1.0 "

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": USER_AGENT})

def get_first_valid_link(soup):
    """
    From a Wikipedia page soup, extract the first valid link in the introduction.
    Requirements:
    - Must be the FIRST link
    - Must NOT be in parentheses
    - Must NOT be in italic (<i> or <em>)
    - Must link to another article (/wiki/...)
    - Must ignore links like Help:, File:, Special:, etc.
    """

    content = soup.find("div", {"id": "mw-content-text"})
    #print(f"------>{content}")

    if not content:
        return None

    # The introduction is made of consecutive <p> tags before any <h2>
    paragraphs = []
    for elem in content.select('p > a'):
        if elem.name == 'h2':
            break
        paragraphs.append(elem)

    parentheses_depth = 0
    print(paragraphs)

    for p in paragraphs:
        print(p)
        for element in p.descendants:
            # Check if it's a link
            # print(element)
            if element.name == 'a':
                href = element.get('href')

                if not href:
                    continue

                # Must link to a real Wikipedia article
                if not href.startswith("/wiki/"):
                    continue
                if any(href.startswith(prefix) for prefix in [
                    "/wiki/Help:",
                    "/wiki/Special:",
                    "/wiki/Talk:",
                    "/wiki/File:",
                    "/wiki/Wikipedia:",
                    "/wiki/Template:",
                    "/wiki/Category:",
                ]):
                    continue

                # Ignore links in parentheses
                if parentheses_depth > 0:
                    continue

                # Success!
                return "https://en.wikipedia.org" + href

    return None



def extract_title(soup):
    """Return the main title of the Wikipedia page."""
    # print(soup)
    title = soup.find(id= "firstHeading")
    print(title)
    return title.text.strip() if title else None



def check_redirection(soup):
    """
    Detect Wikipedia non-URL redirection messages:
       'redirected from <something>'
    If found, return the target link.
    """
    redirect = soup.find("div", {"class": "redirectMsg"})
    print(redirect)
    if redirect:
        link = redirect.find("a")
        if link and link.get("href"):
            return "https://en.wikipedia.org" + link.get("href")
    return None



def fetch_page(url):
    """Download a Wikipedia page and return a BeautifulSoup object."""
    print(url)
    response = SESSION.get(url)
    print(response.status_code)
    return BeautifulSoup(response.text, "html.parser")



def main():
    if len(sys.argv) != 2:
        print("Usage: python3 roads_to_philosophy.py 'your search term'")
        sys.exit(1)

    search = sys.argv[1].replace(" ", "_")
    visited = []

    current_url = WIKIPEDIA_URL + search

    while True:
        soup = fetch_page(current_url)

        # Handle redirection (non-URL)
        redirect_target = check_redirection(soup)
        if redirect_target:
            current_url = redirect_target
            soup = fetch_page(current_url)

        title = extract_title(soup)
        print(f"=======> {title}")
        if not title:
            print("It leads to a dead end !")
            return

        print(title)
        visited.append(title)

        # Check infinite loop
        if len(visited) != len(set(visited)):
            print("It leads to an infinite loop !")
            return

        # Check if reached Philosophy
        if current_url == PHILOSOPHY_URL:
            print(f"{len(visited)} roads from {visited[0]} to philosophy")
            return

        # Get first valid link from introduction
        next_link = get_first_valid_link(soup)
        if not next_link:
            print("It leads to a dead end !")
            return

        current_url = next_link



if __name__ == "__main__":
    main()
