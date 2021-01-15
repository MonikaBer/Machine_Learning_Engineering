from sklearn.ensemble import RandomForestRegressor 
from sklearn.model_selection import train_test_split, RandomizedSearchCV
import numpy as np


class Model:

    def test(self, predictions, test_data = True):
        if test_data:
            labels = self.test_labels
        else:
            labels = self.train_labels
        self.show_mean_absolute_error(predictions, labels)
        self.show_mean_square_error(predictions, labels)
        self.show_accuracy(predictions, labels)


    def show_mean_absolute_error(self, predictions, labels):
        mae = abs(predictions - labels)
        print(f'Mean absolute error: {round(np.mean(mae), 2)} degrees')


    def show_mean_square_error(self, predictions, labels):
        mse = (np.square(predictions - labels))
        print(f'Mean square error: {round(np.mean(mse), 2)}')


    def show_accuracy(self, predictions, labels):
        """
        Accuracy jest rozumiane jako procent predykcji bliższych poprawnej odpowiedzi niż niepoprawnej.
        Dla danych czysto losowych otrzymujemy accuracy 50%
        """
        wrong_or_correct_preds = np.round(predictions, 0) - labels
        wrong_preds_num = np.count_nonzero(wrong_or_correct_preds)
        correct_preds_num = len(predictions) - wrong_preds_num

        accuracy = round(100*correct_preds_num/len(predictions), 3)
        print(f'Correct predictions: {correct_preds_num}/{len(predictions)}. Accuracy: {accuracy}%')


    def show_dataset_shapes(self):
        print('\nTraining Features Shape:', self.train_features.shape)
        print('Training Labels Shape:', self.train_labels.shape)
        print('Testing Features Shape:', self.test_features.shape)
        print('Testing Labels Shape:', self.test_labels.shape, '\n')
        


class BasicModel(Model):
    def __init__(self, dataset):
        features, labels = dataset
        self.train_features, self.test_features, self.train_labels, self.test_labels = train_test_split(features, labels, test_size = 0.20, random_state = 42) 


    def train(self):
        """"Udaje zaawansowany model - w rzeczywistosci nie potrzebuje uczenia"""
        print('"Training" complete')


    def test(self, test_data = True):
        if test_data:
            constant_prediction = int(np.count_nonzero(self.test_labels) / len(self.test_labels) > 0.5)
            predictions = [constant_prediction for _ in self.test_features]
        else:
            constant_prediction = int(np.count_nonzero(self.train_labels) / len(self.train_labels) > 0.5)
            predictions = [constant_prediction for _ in self.train_features]

        super().test(predictions, test_data)


class AdvancedModel(Model):
    def __init__(self, dataset, best_params_search = False):
        features, labels = dataset
        self.train_features, self.test_features, self.train_labels, self.test_labels = train_test_split(features, labels, test_size = 0.20, random_state = 42) 
        if not best_params_search: 
            self.regressor = RandomForestRegressor(n_estimators = 200, random_state = 42, max_depth = 7)
        else:
            parameters = {'n_estimators': [50*x for x in range(1, 4)],
                'min_samples_split': [5*x for x in range(1,15,2)],
                'min_samples_leaf': [2*x+1 for x in range(14)],
                'max_leaf_nodes': [2*x for x in range(1, 9)],
                'max_depth': [2*x for x in range(1,5)]}

            grid_search = RandomizedSearchCV(RandomForestRegressor(random_state=71830), param_distributions=parameters)

            # Dokonujemy przeszukiwania po wszystkich możliwościach parametrów
            grid_search.fit(features, labels)

            self.regressor = RandomForestRegressor(**grid_search.best_params_)
            print("Best params:")
            print(grid_search.best_params_)


    def train(self):
        self.regressor.fit(self.train_features, self.train_labels)
        print('Training complete')


    def test(self, test_data = True):
        if test_data: 
            predictions = self.regressor.predict(self.test_features)
        else: 
            predictions = self.regressor.predict(self.train_features)
        super().test(predictions, test_data)


    #serve prediction
    def predict(self, features):
        preds = self.regressor.predict(features)
        return preds[0]