from flask import Blueprint, request, jsonify
from backend.utils.scraper import get_google_results

search_bp = Blueprint('search', __name__)

@search_bp.route('/search', methods=['POST', 'OPTIONS'])
def buscar():
    if request.method == 'OPTIONS':
        return '', 200  # Respuesta CORS preflight OK

    data = request.get_json()
    query = data.get("query")
    sites = data.get("sites", [])
    min_price = data.get("minPrice")
    max_price = data.get("maxPrice")

    if not query or not sites:
        return jsonify({"error": "Missing query or sites"}), 400

    resultados = []
    for site in sites:
        resultados += get_google_results(query, site)

    # Filtro por precio si está definido
    if min_price is not None or max_price is not None:
        def filtrar_por_precio(item):
            precio_raw = item.get("price")
            if not precio_raw:
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
