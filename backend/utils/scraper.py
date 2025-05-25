from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re

class Product:
    def __init__(self, title, price, url, snippet='', image=None):
        self.title = title
        self.price = price
        self.url = url
        self.snippet = snippet
        self.image = image

    def to_dict(self):
        return {
            "title": self.title,
            "price": self.price,
            "url": self.url,
            "snippet": self.snippet,
            "image": self.image,
        }

class GoogleScraper:
    def __init__(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--log-level=3")
        self.driver = webdriver.Chrome(options=options)

    def search_google(self, query: str, site: str, start=0, aggressive=True) -> BeautifulSoup:
        if aggressive:
            hacking_query = (
                f'site:{site} inurl:producto OR inurl:product "{query}" '
                f'("€" | "EUR") intitle:{query.split()[0]} -"forum" -"pdf" -"blog"'
            )
        else:
            hacking_query = f'site:{site} "{query}"'

        url = f"https://www.google.com/search?q={hacking_query}&start={start}"
        print(f"[🔎 URL] {url}")
        self.driver.get(url)
        time.sleep(2)
        return BeautifulSoup(self.driver.page_source, 'html.parser')

    def extract_price(self, text: str) -> str:
        match = re.search(r'(\d{1,3}(?:[\.,]\d{3})*[\.,]?\d{2}) ?€', text)
        return f"{match.group(1)} €" if match else "Precio no disponible"

    def extract_results(self, soup: BeautifulSoup) -> list:
        seen = set()
        results = []

        for res in soup.select('div.g, div.tF2Cxc, div.MjjYud'):
            a_tag = res.find('a', href=True)
            if not a_tag:
                continue

            url = a_tag['href']
            if url.startswith('/url?q='):
                url = url.split('/url?q=')[1].split('&')[0]

            if url in seen or not url.startswith('http'):
                continue
            seen.add(url)

            title_tag = res.find('h3')
            title = title_tag.get_text(strip=True) if title_tag else 'Sin título'

            desc = res.get_text(" ", strip=True)
            price = self.extract_price(desc)

            img_tag = res.select_one('img')
            image = img_tag['src'] if img_tag and img_tag.get('src', '').startswith('http') else None

            product = Product(title=title, price=price, url=url, snippet=desc[:250], image=image)
            results.append(product)

        return results

    def get_results(self, query: str, site: str, pages=3, aggressive=True):
        results = []
        for i in range(pages):
            print(f"[🔁 Página {i+1}]")
            soup = self.search_google(query, site, start=i * 10, aggressive=aggressive)
            results += self.extract_results(soup)
            time.sleep(1)
        return results

    def close(self):
        self.driver.quit()

# Función pública que puede usar Flask o test_scraper.py
def get_google_results(query, site):
    scraper = GoogleScraper()
    try:
        products = scraper.get_results(query, site, pages=3, aggressive=True)
        return [p.to_dict() for p in products]
    finally:
        scraper.close()
