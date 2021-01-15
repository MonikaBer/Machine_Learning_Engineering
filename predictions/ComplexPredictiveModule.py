import os
import json
import numpy as np
from predictions.Session import Session

class ComplexPredictiveModule:
    def __init__(self, complex_model, historical_data):
        self.complex_model = complex_model
        self.historical_data = historical_data


    def load_input_data(self, input_filename):
        self.open_sessions = []

        with open(input_filename, 'r') as f:
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
                session = Session(curr_session_id, activities, self.historical_data.users, self.historical_data.products, finished=False)
                self.open_sessions.append(session)
                activities = []
                curr_session_id = line_dict_list[i]['session_id']
                activities.append(line_dict_list[i])
            i += 1


    def build_features(self):
        self.features = np.array([(
                            len(s.activities),
                            self.count_user_custom(s),
                            self.count_product_buying_frequency(s),
                            ) 
                            for s in self.open_sessions])


    def predict(self):
        labels = self.complex_model.predict(self.features)
        
        i = 0
        for s in self.open_sessions:
            s.if_buy = labels[i]
            i += 1


    def show_result(self):
        print('Probability that session will be finished with BUY:\n\n') 
        for s in self.open_sessions:
            if s.if_buy is None:
                print(f'Session_id = {s.session_id} -> UNKNOWN')
            else:
                print(f'Session_id = {s.session_id} -> {round(s.if_buy*100, 2)} %')


    def count_user_custom(self, session):
        if session.user_id is None:
            return 0

        buy_sessions = 0
        all_sessions = 0
        for s in self.historical_data.sessions:
            if s.user_id == session.user_id:
                all_sessions += 1
                if s.if_buy == 1.0:
                     buy_sessions += 1

        if all_sessions == 0:
            return 0

        return buy_sessions / all_sessions       


    def count_product_buying_frequency(self, session):
        last_product_id = session.activities[-1].product_id
        if last_product_id is None:
            return 0

        was_in_session_counter = 0
        bought_in_session_counter = 0

        def was_in_session(session, product_id):
            for a in session.activities:
                if a.product_id == product_id:
                    return True
            return False

        def bought_in_session(session, product_id):
            if session.if_buy == 1.0 and session.activities[-1].product_id == product_id:
                return True
            return False

        for s in self.historical_data.sessions:
            if was_in_session(s, last_product_id):
                was_in_session_counter += 1
            if bought_in_session(s, last_product_id):
                bought_in_session_counter += 1
            
        return bought_in_session_counter / was_in_session_counter
