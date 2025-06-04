from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from backend.modelos.product import Product
from backend.utils.logger import get_logger

# Logger para seguimiento
logger = get_logger("google")

class GoogleScraper:
    def __init__(self):
         #Configura el navegador
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--log-level=3")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
        )
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def build_query(self, query, site, mode="aggressive"):
        # Construye la consulta con filtros
        base_query = f'site:{site} "{query}"'
        if mode == "title":
            return f'site:{site} intitle:"{query}"'
        elif mode == "aggressive":
            return f'{base_query} (EUR OR € OR precio)'
        else:
            return base_query

    def search_google(self, query: str, site: str, start=0, engine="google", mode="aggressive") -> BeautifulSoup:
        # Realiza la busqueda y devuelve el html parseadp con las plantillas (cards)
        hacking_query = self.build_query(query, site, mode)

        if engine == "bing":
            url = f"https://www.bing.com/search?q={hacking_query}"
        elif engine == "duckduckgo":
            url = f"https://html.duckduckgo.com/html/?q={hacking_query}"
        else:
            url = f"https://www.google.com/search?q={hacking_query}&start={start}"

        logger.info(f"[Página {int(start / 10) + 1}] {hacking_query}")

        self.driver.get(url)
        time.sleep(3)

        # Acepta cookies si aparece el modal
        try:
            accept_btn = self.driver.find_element("xpath", "//button[contains(text(), 'Aceptar') or contains(text(), 'Accept')]")
            accept_btn.click()
            logger.info("[Cookies aceptadas]")
            time.sleep(1)
        except:
            logger.info("[Sin modal de cookies o ya aceptado]")

        html = self.driver.page_source

        # Detecta si hay captcha 
        if "detected unusual traffic" in html.lower() or "solve the captcha" in html.lower():
            raise Exception("CaptchaDetected")

        return BeautifulSoup(html, 'html.parser')

    def extract_price(self, text: str) -> str:
    # Extrae precio en formato € desde un texto
        match = re.search(r'(\d{1,3}(?:[\.,]\d{3})*[\.,]?\d{2}) ?€', text)
        return f"{match.group(1)} €" if match else "Precio no disponible"

    def extract_results(self, soup: BeautifulSoup, engine="google") -> list:
        # Extrae resultados desde el HTML
        seen = set()
        results = []

        if engine == "bing":
            result_blocks = soup.select('li.b_algo')
        elif engine == "duckduckgo":
            result_blocks = soup.select('div.result')
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

            title_tag = res.find('h2') if engine in ["bing", "duckduckgo"] else res.find('h3')
            title = title_tag.get_text(strip=True) if title_tag else 'Sin título'

            desc = res.get_text(" ", strip=True)
            price = self.extract_price(desc)

            img_tag = res.select_one('img')
            image = img_tag['src'] if img_tag and img_tag.get('src', '').startswith('http') else None

            product = Product(title=title, price=price, url=url, snippet=desc[:250], image=image)
            results.append(product)

        logger.info(f"[Resultados encontrados] {len(results)}")
        return results

    def get_results(self, query: str, site: str, pages=3, engine="google", mode="aggressive"):
        # Busca en varias paginas y acumula resultados
        results = []
        for i in range(pages):
            try:
                soup = self.search_google(query, site, start=i * 10, engine=engine, mode=mode)
                new_results = self.extract_results(soup, engine=engine)
                results += new_results

                # Fallback a Google si DuckDuckGo no da resultados
                if engine == "duckduckgo" and not new_results:
                    logger.warning("[DuckDuckGo vacío] Probando con Google como respaldo")
                    soup = self.search_google(query, site, start=i * 10, engine="google", mode=mode)
                    results += self.extract_results(soup, engine="google")

            except Exception as e:
                logger.error(f"[Error en página {i + 1}] {str(e)}")
            time.sleep(1)
        return results

    def close(self):
                # Cierra el navegador
        self.driver.quit()


def get_google_results(query, site, engine="google", mode="aggressive"):
        # Función externa para obtener resultados como diccionarios

    scraper = GoogleScraper()
    try:
        products = scraper.get_results(query, site, pages=3, engine=engine, mode=mode)
        return [p.to_dict() for p in products]
    except Exception as e:
        logger.error(f"Error en el scraper: {e}")
        if "CaptchaDetected" in str(e):
            return {"error": "captcha"}
        raise
    finally:
        scraper.close()