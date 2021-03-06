
class PredictiveModule:
    def __init__(self, model):
        self.model = model


    def load_data(self, open_sessions):
        self.open_sessions = open_sessions

    def show_result(self):
        print('\nProbability that session will be finished with BUY:\n') 
        for s in self.open_sessions:
            if s.if_buy is None:
                print(f'Session_id = {s.session_id} -> UNKNOWN')
            else:
                print(f'Session_id = {s.session_id} -> {round(s.if_buy*100, 2)} %')  


    def save_result(self, result_filename):
        with open(result_filename, 'a') as f:
            for s in self.open_sessions:
                if not s.for_AB_exp:
                    continue

                if s.if_buy is None:   
                    f.write('{"session_id": ' + str(s.session_id) + 
                            ', "prediction": null, "user_id": ' + str(s.user_id) + 
                            ', "session_length": ' + str(len(s.activities)) + 
                            '}\n')
                else:
                    f.write('{"session_id": ' + str(s.session_id) + 
                            ', "prediction": ' + str(round(s.if_buy*100, 2)) + 
                            ', "user_id": ' + str(s.user_id) + 
                            ', "session_length": ' + str(len(s.activities)) + 
                            '}\n')
                    