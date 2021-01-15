from predictions.PredictiveModule import PredictiveModule

class BasicPredictiveModule(PredictiveModule):
    def __init__(self, basic_model):
        super().__init__(basic_model)


    def predict(self):
        labels = self.model.predict(self.open_sessions)
        
        i = 0
        for s in self.open_sessions:
            s.if_buy = labels[i]
            i += 1


    def show_result(self):
        print('\n-----BASIC-MODEL -PREDICTIONS-----:\n')
        super().show_result()
