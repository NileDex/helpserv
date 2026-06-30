"""
RSU Web Scraper
---------------
Scrapes Rivers State University pages and saves structured data
to data/scraped_rsu.json for use in the knowledge base.

Run:
    py -3.12 scraper.py
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
import os

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

PAGES = {
    'home':              'https://www.rsu.edu.ng/',
    'about':             'https://www.rsu.edu.ng/about-us/',
    'contact':           'https://www.rsu.edu.ng/contact/',
    'location':          'https://www.rsu.edu.ng/location/',
    'vice_chancellor':   'https://www.rsu.edu.ng/vice-chancellor/',
    'pro_chancellor':    'https://www.rsu.edu.ng/profile-of-pro-chancellor-and-chairman-of-council/',
    'professorial_chairs': 'https://www.rsu.edu.ng/professorial-chairs/',
    'news':              'https://www.rsu.edu.ng/news-update/',
    'events':            'https://www.rsu.edu.ng/event-calendar/',
    'lectures':          'https://www.rsu.edu.ng/lectures/',
    'course_clinical':   'https://www.rsu.edu.ng/course/basic-clinical-sciences/',
    'course_medical':    'https://www.rsu.edu.ng/course/basic-medical-sciences/',
    'course_faculty':    'https://www.rsu.edu.ng/course/faculty-of-clinical-sciences/',
    'strategic_plan':    'https://www.rsu.edu.ng/strategic-development-plan-final-march-2026/',
    'ecampus':           'https://ecampus.rsu.edu.ng/',
}

# Tags that are noise — remove before extracting text
NOISE_TAGS = ['script', 'style', 'nav', 'footer', 'header',
              'aside', 'iframe', 'noscript', 'form']


def clean(text: str) -> str:
    text = re.sub(r'[ \t]{2,}', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def scrape_page(url: str) -> dict | None:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=20)
        resp.raise_for_status()
    except Exception as e:
        print(f'    ERROR: {e}')
        return None

    soup = BeautifulSoup(resp.text, 'html.parser')

    # Strip noise
    for tag in soup(NOISE_TAGS):
        tag.decompose()

    # Find main content area (try several common selectors)
    main = (
        soup.find('main') or
        soup.find('article') or
        soup.find('div', class_=re.compile(r'\b(content|entry|post|page-content)\b', re.I)) or
        soup.find('div', id=re.compile(r'\b(content|main|primary)\b', re.I)) or
        soup.body
    )

    if not main:
        return None

    title = soup.title.get_text(strip=True) if soup.title else ''
    headings = [h.get_text(strip=True) for h in main.find_all(['h1', 'h2', 'h3', 'h4']) if h.get_text(strip=True)]
    paragraphs = [p.get_text(strip=True) for p in main.find_all('p') if p.get_text(strip=True)]
    lists = []
    for ul in main.find_all(['ul', 'ol']):
        items = [li.get_text(strip=True) for li in ul.find_all('li') if li.get_text(strip=True)]
        if items:
            lists.append(items)

    full_text = clean(main.get_text(separator='\n', strip=True))

    return {
        'url': url,
        'title': title,
        'headings': headings[:20],       # cap to avoid noise
        'paragraphs': paragraphs[:30],
        'lists': lists[:10],
        'full_text': full_text[:5000],   # first 5000 chars is enough for KB
    }


def run():
    out_path = os.path.join(os.path.dirname(__file__), 'data', 'scraped_rsu.json')
    results = {}
    total = len(PAGES)

    print(f'\nScraping {total} RSU pages...\n')

    for i, (key, url) in enumerate(PAGES.items(), 1):
        print(f'[{i}/{total}] {key}')
        print(f'    {url}')
        data = scrape_page(url)
        if data:
            results[key] = data
            print(f'    OK  ({len(data["full_text"])} chars, {len(data["headings"])} headings)')
        else:
            print(f'    SKIPPED')
        time.sleep(1.5)   # polite delay between requests

    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f'\nDone. {len(results)}/{total} pages saved to data/scraped_rsu.json')
    print('Run app.py — the knowledge base will load the scraped data automatically.')


if __name__ == '__main__':
    run()
