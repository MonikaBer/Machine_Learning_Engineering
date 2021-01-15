

class BasicPredictiveModule:
    def __init__(self, basic_model):
        self.basic_model = basic_model


    def load_data(self, open_sessions):
        self.open_sessions = open_sessions


    def predict(self):
        labels = self.basic_model.predict(self.open_sessions)
        
        i = 0
        for s in self.open_sessions:
            s.if_buy = labels[i]
            i += 1


    def show_result(self):
        print('\n-----BASIC-MODEL -PREDICTIONS-----:\n')
        print('\nProbability that session will be finished with BUY:\n') 
        for s in self.open_sessions:
            if s.if_buy is None:
                print(f'Session_id = {s.session_id} -> UNKNOWN')
            else:
                print(f'Session_id = {s.session_id} -> {round(s.if_buy*100, 2)} %')

    def save_result(self, result_filename):
        with open(result_filename, 'w') as f:
            for s in self.open_sessions:
                if s.if_buy is None:   
                    f.write('{"session_id": ' + str(s.session_id) + ', "result": null, "user_id": ' + str(s.user_id) + '}\n')
                else:
                    f.write('{"session_id": ' + str(s.session_id) + ', "result": ' + str(round(s.if_buy*100, 2)) + ', "user_id": ' + str(s.user_id) + '}\n')
                    