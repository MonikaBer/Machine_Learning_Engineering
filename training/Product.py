
class Product:
    
    def __init__(self, product_id, product_name, category_path, price, rating):
        self.product_id = product_id
        self.product_name = product_name
        self.category_path = category_path
        try:
            self.rating = float(rating)
        except:
            raise ValueError
        try:
            self.price = int(price)
        except:
            raise ValueError
        self.frequency = None
