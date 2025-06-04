#Represemta el producto
class Product:
    def __init__(self, title, price, url, snippet='', image=None):
        # Inicializa el producto con sus datos
        self.title = title
        self.price = price
        self.url = url
        self.snippet = snippet
        self.image = image

    #Devuelve el producto pero como diccionario
    def to_dict(self):
        return {
            "title": self.title,
            "price": self.price,
            "url": self.url,
            "snippet": self.snippet,
            "image": self.image,
        }
