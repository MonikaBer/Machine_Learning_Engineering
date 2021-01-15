import json
from predictions.Product import Product
from predictions.Session import Session

class HistoricalData:

    def __init__(self, products_filename, users_filename, sessions_filename):    
        self.products = []
        self.users = []
        self.sessions = []

        self.init_products(products_filename)
        self.init_users(users_filename)
        self.init_sessions(sessions_filename)


    def init_products(self, products_filename):
        with open(products_filename, 'r') as f:
            line_dict_list = []
            for line in f:
                line_dict = json.loads(line)
                line_dict_list.append(line_dict)

        if len(line_dict_list) == 0:
            return

        for line_dict in line_dict_list:
            product = Product(line_dict['product_id'], line_dict['rating'])
            self.products.append(product)


    def init_users(self, users_filename):
        with open(users_filename, 'r') as f:
            line_dict_list = []
            for line in f:
                line_dict = json.loads(line)
                line_dict_list.append(line_dict)

        if len(line_dict_list) == 0:
            return

        for line_dict in line_dict_list:
            self.users.append(line_dict['user_id'])


    def init_sessions(self, sessions_filename):
        with open(sessions_filename, 'r') as f:
            line_dict_list = []
            for line in f:
                line_dict = json.loads(line)
                line_dict_list.append(line_dict)

        if len(line_dict_list) == 0:
            return

        activities = []
        i = 0
        curr_session_id = line_dict_list[i]['session_id']
        activities.append(line_dict_list[i])

        i = 1
        while i < len(line_dict_list):
            if curr_session_id == line_dict_list[i]['session_id']:
                activities.append(line_dict_list[i])
            else:
                session = Session(curr_session_id, activities, self.users, self.products, finished=True)
                self.sessions.append(session)
                activities = []
                curr_session_id = line_dict_list[i]['session_id']
                activities.append(line_dict_list[i])
            i += 1

        if len(activities) != 0:
            session = Session(curr_session_id, activities, self.users, self.products, finished=True)
            self.sessions.append(session)


    # def show_products(self):
    #     for product in self.products:
    #         print(f'product id = {product.product_id}, rating = {product.rating}\n')


    # def show_users(self):
    #     for user in self.users:
    #         print(f'user id = {user.user_id} \n')
