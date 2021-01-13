from sklearn.ensemble import RandomForestRegressor 
from sklearn.model_selection import train_test_split
import numpy as np


class Model:
    def __init__(self, dataset):
        features, labels = dataset
        self.train_features, self.test_features, self.train_labels, self.test_labels = train_test_split(features, labels, test_size = 0.25, random_state = 42) 
        self.regressor = RandomForestRegressor(n_estimators = 100, random_state = 0) 


    def train(self):
        self.regressor.fit(self.train_features, self.train_labels)
        print('Training complete')


    def test(self, show_accuracy = False):
        predictions = self.regressor.predict(self.test_features)
        self.show_mean_square_error(predictions)
        if show_accuracy: self.show_accuracy(predictions)


    def show_mean_square_error(self, predictions):
        mse = (np.square(predictions - self.test_labels)).mean()
        print(f'Mean square error: {round(mse, 4)}')


    def show_accuracy(self, predictions):
        """
        Accuracy jest rozumiane jako procent predykcji bliższych poprawnej odpowiedzi niż niepoprawnej.
        Dla danych czysto losowych otrzymujemy accuracy 50%
        """
        wrong_or_correct_preds = np.round(predictions, 0) - self.test_labels
        wrong_preds_num = np.count_nonzero(wrong_or_correct_preds)
        correct_preds_num = len(predictions) - wrong_preds_num

        accuracy = round(100*correct_preds_num/len(predictions), 3)
        print(f'Correct predictions: {correct_preds_num}/{len(predictions)}. Accuracy: {accuracy}%')


    def show_dataset_shapes(self):
        print('\nTraining Features Shape:', self.train_features.shape)
        print('Training Labels Shape:', self.train_labels.shape)
        print('Testing Features Shape:', self.test_features.shape)
        print('Testing Labels Shape:', self.test_labels.shape, '\n')
