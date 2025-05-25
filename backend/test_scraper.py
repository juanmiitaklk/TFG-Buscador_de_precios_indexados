from utils.scraper import get_google_results
import json

if __name__ == "__main__":
    query = input("🔎 Escribe el producto a buscar: ")
    site = input("🌐 Escribe el dominio de la tienda (ej. pccomponentes.com): ")

    print("\n⏳ Buscando productos...")
    resultados = get_google_results(query, site)

    print(f"\n✅ Se encontraron {len(resultados)} resultados.\n")

    for i, item in enumerate(resultados, 1):
        print(f"{i}. {item['title']}")
        print(f"   🏷️  Precio: {item['price']}")
        print(f"   🔗 URL: {item['url']}")
        print(f"   📄 Snippet: {item['snippet'][:100]}...")
        print(f"   🖼️  Imagen: {item['image'] if item['image'] else 'No encontrada'}")
        print("-" * 80)

    # Exportar como JSON si quieres guardarlo
    with open("resultados_test.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
        print("\n📝 Resultados guardados en resultados_test.json")
