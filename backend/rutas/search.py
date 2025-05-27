from flask import Blueprint, request, jsonify
from backend.utils.scraper import get_google_results

search_bp = Blueprint('search', __name__)

@search_bp.route('/search', methods=['POST'])
def buscar():
    data = request.get_json()
    query = data.get("query")
    sites = data.get("sites", [])
    min_price = data.get("minPrice")
    max_price = data.get("maxPrice")
    engine = data.get("engine", "google")  # Por defecto: Google

    if not query or not sites:
        return jsonify({"error": "Missing query or sites"}), 400

    resultados = []
    for site in sites:
        resultado = get_google_results(query, site, engine=engine)
        if isinstance(resultado, dict) and resultado.get("error") == "captcha":
            return jsonify({"error": "captcha"}), 200
        resultados += resultado

    # Filtro por precio si viene definido
    if min_price is not None or max_price is not None:
        def filtrar_por_precio(item):
            precio_raw = item.get("price")
            if not precio_raw or precio_raw == "Precio no disponible":
                return False
            try:
                precio_str = (
                    precio_raw.replace("€", "")
                    .replace(".", "")
                    .replace(",", ".")
                    .strip()
                )
                precio = float(precio_str)
            except:
                return False

            if min_price is not None and precio < min_price:
                return False
            if max_price is not None and precio > max_price:
                return False

            return True

        resultados = list(filter(filtrar_por_precio, resultados))

    return jsonify(resultados)
