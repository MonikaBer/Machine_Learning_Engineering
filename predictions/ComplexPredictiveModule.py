import numpy as np
from predictions.PredictiveModule import PredictiveModule

class ComplexPredictiveModule(PredictiveModule):
    def __init__(self, complex_model, historical_data):
        super().__init__(complex_model)
        self.historical_data = historical_data


    def build_features(self):
        self.features = np.array([(
                            len(s.activities),
                            self.count_user_custom(s),
                            self.count_product_buying_frequency(s),
                            self.get_product_rating(s)
                            ) 
                            for s in self.open_sessions])


    def predict(self):
        labels = self.model.predict(self.features)
        
        i = 0
        for s in self.open_sessions:
            s.if_buy = labels[i]
            i += 1


    def show_result(self):
        print('\n-----COMPLEX-MODEL -PREDICTIONS-----:\n')
        super().show_result()    


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

        if was_in_session_counter == 0:
            return 0  
        return bought_in_session_counter / was_in_session_counter

    def get_product_rating(self, session):
        last_product_id = session.activities[-1].product_id

        if last_product_id is None:
            return 0

        for p in self.historical_data.products:
            if p.product_id == last_product_id:
                return p.rating
        
        return 0
