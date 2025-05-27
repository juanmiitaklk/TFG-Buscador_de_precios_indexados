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

    def search_google(self, query: str, site: str, start=0, engine="google", aggressive=True) -> BeautifulSoup:
        if aggressive:
            hacking_query = f'site:{site} intext:"{query}" ("€" | "EUR")'
        else:
            hacking_query = f'site:{site} "{query}"'

        if engine == "bing":
            url = "https://www.bing.com/search?q=" + hacking_query
        else:
            url = "https://www.google.com/search?q=" + hacking_query + f"&start={start}"

        print(f"[🔁 Página {int(start / 10) + 1}]")
        print(f"[🔎 SENTENCIA] {hacking_query}")

        self.driver.get(url)
        time.sleep(2)

        # Aceptar cookies en Google
        if engine == "google":
            try:
                accept_btn = self.driver.find_element("xpath", "//button//div[contains(text(), 'Aceptar todo')]")
                accept_btn.click()
                print("[✅ Google - Cookies aceptadas]")
                time.sleep(1)
            except:
                print("[ℹ️ Google - Sin modal de cookies o ya aceptado]")

        # Aceptar cookies en Bing
        if engine == "bing":
            try:
                accept_btn = self.driver.find_element("xpath", "//button[contains(., 'Aceptar')]")
                accept_btn.click()
                print("[✅ Bing - Cookies aceptadas]")
                time.sleep(1)
            except:
                print("[ℹ️ Bing - Sin modal de cookies o ya aceptado]")

        filename = f"screenshot_{engine}_{site.replace('.', '_')}_{start}.png"
        self.driver.save_screenshot(filename)
        print(f"[📸 Captura guardada] {filename}")

        html = self.driver.page_source
        print(f"[💡 HTML Length] {len(html)}")

        if "detected unusual traffic" in html.lower() or "solve the captcha" in html.lower():
            raise Exception("CaptchaDetected")

        return BeautifulSoup(html, 'html.parser')

    def extract_price(self, text: str) -> str:
        match = re.search(r'(\d{1,3}(?:[\.,]\d{3})*[\.,]?\d{2}) ?€', text)
        return f"{match.group(1)} €" if match else "Precio no disponible"

    def extract_results(self, soup: BeautifulSoup, engine="google") -> list:
        seen = set()
        results = []

        if engine == "bing":
            result_blocks = soup.select('li.b_algo')
        else:
            result_blocks = soup.select('div.g, div.tF2Cxc, div.MjjYud')

        for res in result_blocks:
            a_tag = res.find('a', href=True)
            if not a_tag:
                continue

            url = a_tag['href']
            if url.startswith('/url?q='):
                url = url.split('/url?q=')[1].split('&')[0]

            if url in seen or not url.startswith('http'):
                continue
            seen.add(url)

            title_tag = res.find('h2') if engine == "bing" else res.find('h3')
            title = title_tag.get_text(strip=True) if title_tag else 'Sin título'

            desc = res.get_text(" ", strip=True)
            price = self.extract_price(desc)

            img_tag = res.select_one('img')
            image = img_tag['src'] if img_tag and img_tag.get('src', '').startswith('http') else None

            product = Product(title=title, price=price, url=url, snippet=desc[:250], image=image)
            results.append(product)

        print(f"[✅ Resultados encontrados] {len(results)}")
        return results

    def get_results(self, query: str, site: str, pages=3, engine="google", aggressive=True):
        results = []
        for i in range(pages):
            soup = self.search_google(query, site, start=i * 10, engine=engine, aggressive=aggressive)
            results += self.extract_results(soup, engine=engine)
            time.sleep(1)
        return results

    def close(self):
        self.driver.quit()

def get_google_results(query, site, engine="google", aggressive=True):
    scraper = GoogleScraper()
    try:
        products = scraper.get_results(query, site, pages=3, engine=engine, aggressive=aggressive)
        return [p.to_dict() for p in products]
    except Exception as e:
        if "CaptchaDetected" in str(e):
            return {"error": "captcha"}
        raise
    finally:
        scraper.close()
