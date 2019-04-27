def loadProductfromJSON(dict):
    short_description = dict.get('short_description', None)
    description = dict.get('description', None)
    features = dict.get('features', None)
    standard_price = dict.get('standard_price', None)
    price = dict.get('price', None)
    url = dict.get('url', None)
    image_url = dict.get('image_url', None)
    end_date = dict.get('end_date', None)
    size = dict.get('size', None)

    return Product(short_description=short_description,
                    description=description,
                    features=features,
                    standard_price=standard_price,
                    price=price,
                    url=url,
                    image_url=image_url,
                    end_date=end_date,
                    size=size
                   )

class Product:
    def __init__(self,
                 short_description=None,
                 description=None,
                 features=None,
                 standard_price=None,
                 price=None,
                 url=None,
                 image_url=None,
                 end_date=None,
                 size=None):

        self.short_description = short_description
        self.description = description
        self.features = features
        self.standard_price = standard_price
        self.price = price
        self.url = url
        self.image_url = image_url
        self.end_date = end_date
        self.size = size

        self.is_completed = bool(short_description) and bool(price) and bool(url) and bool(image_url)

    def __str__(self):
        return f'{self.short_description}\nAntes: {self.standard_price}\nAhora: {self.price}\n{self.description}\nurl: {self.url}\nimage_url: {self.image_url}\nis_completed: {self.is_completed}\nFinalize in: {self.end_date}'

    def to_dict(self):
        p = {
            'shortDescription': self.short_description,
            'description': self.description,
            'features': self.features,
            'standardPrice': self.standard_price,
            'price': self.price,
            'size': self.size,
            'url': self.url,
            'imageUrl': self.image_url,
            'isTemporal': self.end_date is not None,
            'isCompleted': self.is_completed

        }
        return p
