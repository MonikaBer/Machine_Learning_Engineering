import json

from common.Session import Session
from common.Session import EventType
from training.Product import Product
from training.User import User
from training.User import Gender

class DataAnalyser:

    def __init__(self, sessions_filename, products_filename, users_filename):    
        self.sessions = [] 
        self.products = []
        self.users = []

        self.init_sessions(sessions_filename)
        self.init_products(products_filename)
        self.init_users(users_filename)
        self.calculate_purchase_frequences()


    def calculate_purchase_frequences(self):
        """Dla każdego produktu wylicza jego purchase frequency"""
        
        def check_in_session(s, p):
            for a in s.session_activities:
                if a.product_id == p.product_id:
                    return True
            return False

        for p in self.products:
            was_in_session_count = 0
            bought_in_session_count = 0
            for s in self.sessions:
                if check_in_session(s, p):
                    was_in_session_count += 1
                if s.if_buy and s.session_activities[-1].product_id == p.product_id:
                    bought_in_session_count += 1
            p.frequency = 0 if was_in_session_count==0 else bought_in_session_count/was_in_session_count

        
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
                session = Session(curr_session_id, activities)
                self.sessions.append(session)
                activities = []
                curr_session_id = line_dict_list[i]['session_id']
                activities.append(line_dict_list[i])
            i += 1

        if len(activities) != 0:
            session = Session(curr_session_id, activities=)
            self.sessions.append(session)


    def init_products(self, products_filename):
        with open(products_filename, 'r') as f:
            line_dict_list = []
            for line in f:
                line_dict = json.loads(line)
                line_dict_list.append(line_dict)

        if len(line_dict_list) == 0:
            return

        categories = []
        for line_dict in line_dict_list:
            # category_path = (line_dict['category_path'])[:(line_dict['category_path']).index(';')]
            # product = Product(line_dict['product_id'], line_dict['product_name'], category_path, line_dict['price'])
            product = Product(line_dict['product_id'], line_dict['product_name'], line_dict['category_path'], line_dict['price'])
            self.products.append(product)
            categories.append(product.category_path[product.category_path.index(';')])

        self.categories_set = set(categories)

    def init_users(self, users_filename):
        with open(users_filename, 'r') as f:
            line_dict_list = []
            for line in f:
                line_dict = json.loads(line)
                line_dict_list.append(line_dict)

        if len(line_dict_list) == 0:
            return

        cities = []

        for line_dict in line_dict_list:
            user = User(line_dict)
            self.users.append(user)
            cities.append(user.city)

        self.cities_set = set(cities)


    def show_sessions(self):
        for session in self.sessions:
            print("\nsession id = {} duration = {}s :\n".format(session.session_id, session.duration_in_seconds))
            for session_activity in session.session_activities:
                print("timestamp = {}, user id = {}, product id = {}, event type = {}, offered discount = {}\n".format(session_activity.timestamp,
                                                                                                                session_activity.user_id,
                                                                                                                session_activity.product_id,
                                                                                                                session_activity.event_type,
                                                                                                                session_activity.offered_discount))


    def show_products(self):
        for product in self.products:
            print("product id = {}, product name = {}, category path = {}, price = {}, frequency = {} \n".format(product.product_id, 
                                                                                       product.product_name,
                                                                                       product.category_path,
                                                                                       product.price,
                                                                                       product.frequency))


    def show_users(self):
        for user in self.users:
            print("user id = {}, city = {}\n".format(user.user_id, user.city))


    # statistics of BUY and NOT BUY sessions
    def buy_sessions_statistics(self):
        buy_sessions_count = 0
        for session in self.sessions:
            if session.if_buy == True:
                buy_sessions_count += 1

        print("TOTAL = {}, BUY SESSIONS = {}, NOT BUY SESSIONS = {}"
                                            .format(len(self.sessions), buy_sessions_count, len(self.sessions) - buy_sessions_count))


    # check in each BUY SESSION that VIEW precedes BUY
    def how_much_buy_sessions_without_view(self):
        buy_sessions_without_view_count = 0
        
        for session in self.sessions:
            if session.if_buy:
                buy_activity = session.get_buy_session_activity()
                view_activities_assoc_with_buy_activity = session.get_view_activities_assoc_with_buy_activity(buy_activity) 

                if len(view_activities_assoc_with_buy_activity) == 0:
                    buy_sessions_without_view_count += 1

        print("Number of BUY sessions without VIEW events = {}".format(buy_sessions_without_view_count))


    def how_much_unknown_activities(self):
        unknown_activities_count = 0
        for session in self.sessions:
            for activity in session.session_activities:
                if activity.event_type == EventType.UNKNOWN:
                    unknown_activities_count += 1
        
        print("Number of unknown activities = {}".format(unknown_activities_count)) 


    def how_much_sessions_with_more_than_one_user(self):
        count = 0
        for session in self.sessions:
            user_id = None
            for activity in session.session_activities:
                if user_id == None and activity.user_id != None:
                    user_id = activity.user_id
                    continue

                if user_id != None and activity.user_id != None and user_id != activity.user_id:
                    count += 1
                    break

        print("Number of sessions with more than one user = {}".format(count))


    def how_much_null_users(self):
        not_null_user_sessions_count = 0
        for session in self.sessions:
            user_id = None
            for activity in session.session_activities:
                if activity.user_id != None:
                    not_null_user_sessions_count += 1
                    break

        print("Number of sessions with not null user_id = {}".format(not_null_user_sessions_count))        


    def how_much_null_products(self):
        activities_count = 0
        buy_activities_count = 0

        null_products_activities_count = 0
        null_products_in_buy_activities_count = 0
        for session in self.sessions:
            
            for activity in session.session_activities:
                activities_count += 1
                
                if activity.event_type == EventType.BUY:
                    buy_activities_count += 1
                
                if activity.product_id == None:
                    null_products_activities_count += 1
                    
                    if activity.event_type == EventType.BUY:
                        null_products_in_buy_activities_count += 1

        null_products_in_view_activities_count = null_products_activities_count - null_products_in_buy_activities_count
        view_activities_count = activities_count - buy_activities_count

        null_products_in_buy_activities_percent = null_products_in_buy_activities_count / buy_activities_count * 100
        null_products_in_view_activities_percent = null_products_in_view_activities_count / view_activities_count * 100

        print("Number of activities with null product_id = {} / {}\n".format(null_products_activities_count, activities_count)) 
        print("Number of BUY activities with null product_id = {} / {} -> {} %\n".format(null_products_in_buy_activities_count, buy_activities_count, null_products_in_buy_activities_percent))  
        print("Number of VIEW activities with null product_id = {} / {} -> {} %\n".format(null_products_in_view_activities_count, view_activities_count, null_products_in_view_activities_percent))      

    def how_much_incorrect_discounts(self):
        incorrect_discounts_count = 0

        for session in self.sessions:
            for activity in session.session_activities:
                if activity.offered_discount < 0 or activity.offered_discount > 100:
                    incorrect_discounts_count += 1

        print("Number of incorrect discounts = {}".format(incorrect_discounts_count))

    def how_much_incorrect_prices(self):
        negative_prices_count = 0
        large_prices_count = 0

        for product in self.products:
            if product.price < 0:
                negative_prices_count += 1
            elif product.price > 10000:
                large_prices_count += 1

        print("Number of negative prices = {} / {}".format(negative_prices_count, len(self.products)))
        print("Number of prices > 10000 = {} / {}".format(large_prices_count, len(self.products)))

    def are_very_expensive_products_in_buy_sessions(self):
        expensive_products_count = 0

        for session in self.sessions:
            for activity in session.session_activities:
                if activity.event_type == EventType.BUY:
                    for product in self.products:
                        if product.product_id == activity.product_id:
                            if product.price > 10000 and activity.offered_discount < 95:
                                expensive_products_count += 1
                                break
                
        print("Number of very expensive products in BUY sessions = {}".format(expensive_products_count))

    def is_buy_activity_always_at_the_end_of_buy_session(self):
        wrong_sessions_count = 0  # when BUY activity isn't at the end of BUY session 
        for session in self.sessions:
            if session.if_buy == True:
                if session.session_activities[len(session.session_activities) - 1].event_type != EventType.BUY:
                    wrong_sessions_count += 1

        print("Number of BUY sessions in which BUY activity isn't at the end = {}".format(wrong_sessions_count))

    def genders_proportion(self):
        females_count = 0
        males_count = 0
        
        for user in self.users:
            if user.gender == Gender.FEMALE:
                females_count += 1
            elif user.gender == Gender.MALE:
                males_count += 1
        
        unknown_count = len(self.users) - (females_count + males_count)

        print("Number of: females = {}, males = {}, unknown = {}, total = {}".format(females_count, males_count, unknown_count, len(self.users)))
