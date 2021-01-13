
class Product:
    
    def __init__(self, product_id, product_name, category_path, price):
        self.product_id = product_id
        self.product_name = product_name
        self.category_path = category_path
        self.frequency = None
        try:
            self.price = int(price)
        except:
            raise ValueError
