import json

from EventForMicro import EventForMicro
from SessionForMicro import SessionForMicro
from Session import EventType
from ProductForMicro import ProductForMicro
from UserForMicro import UserForMicro

class SystemData:

    def __init__(self, products_filename, users_filename):    
        self.products = []
        self.users = []
        self.ownerless_sessions = []

        self.init_products(products_filename)
        self.init_products(products_filename)


    def init_products(self, products_filename):
        with open(products_filename, 'r') as f:
            line_dict_list = []
            for line in f:
                line_dict = json.loads(line)
                line_dict_list.append(line_dict)

        if len(line_dict_list) == 0:
            return

        for line_dict in line_dict_list:
            product = ProductForMicro(line_dict['product_id'])
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
            user = UserForMicro(line_dict['user_id'])
            self.users.append(user)


    def show_products(self):
        for product in self.products:
            print(f'product id = {product.product_id}\n')


    def show_users(self):
        for user in self.users:
            print(f'user id = {user.user_id} \n')
    

    def put_event_to_history(self, event):
        if event.user_id is None:
            for s in self.ownerless_sessions:
                if s.session_id == event.session_id:
                    s.addEvent(event)
                    return
            new_session = SessionForMicro(event)
            self.ownerless_sessions.append(new_session)
            return
        
        for u in self.users:
            if u.user_id == event.user_id:
                for s in u.sessions_history:
                    if s.session_id == event.session_id:
                        s.addEvent(event)
                        return
                
                new_session = SessionForMicro(event)
                u.sessions_history.append(new_session)
                return


    def get_session_length(self, event):
        if event.user_id is None:
            for s in self.ownerless_sessions:
                if s.session_id == event.session_id:
                    return len(s.events)
            return 0

        for u in self.users:
            if u.user_id == event.user_id:
                for s in u.sessions_history:
                    if s.session_id == event.session_id:
                        return len(s.events)
                return 0
        return 0


    def get_previous_buy_sessions_for_user_proportion(self, event):
        if event.user_id is None:
            return 0

        for u in self.users:
            if u.user_id == event.user_id:
                counter = 0
                for s in u.sessions_history:
                    if s.events[-1].ifBuy:
                        counter += 1
                return counter / len(u.sessions_history)
        
        return 0


    def get_buying_frequency(self, event):
        if event.product_id is None:
            return 0


        def update_counters(session, event, was_in_session_counter, bought_in_session_counter):
            if if_product_in_session(session, event.product_id):
                was_in_session_counter += 1
            if session.events[-1].ifBuy and session.events[-1].product_id == event.product_id:
                bought_in_session_counter += 1

            return was_in_session_counter, bought_in_session_counter


        def if_product_in_session(session, product_id):
            if product_id is None:
                return False
            
            for e in session.events:
                if e.product_id == product_id:
                    return True
            return False


        was_in_session_counter = 0
        bought_in_session_counter = 0

        for p in self.products:
            if p.product_id == event.product_id:
                for s in self.ownerless_sessions:
                    was_in_session_counter, bought_in_session_counter = update_counters(s, 
                                                                                        event, 
                                                                                        was_in_session_counter, 
                                                                                        bought_in_session_counter)

                for u in self.users:
                    for s in u.sessions_history:
                        was_in_session_counter, bought_in_session_counter = update_counters(s, 
                                                                                            event, 
                                                                                            was_in_session_counter, 
                                                                                            bought_in_session_counter)

            if was_in_session_counter == 0:
                return 0
            return bought_in_session_counter / was_in_session_counter
