import os
import joblib

from common.Model import Model
from training.DataAnalyser import DataAnalyser
from training.datasets import *


def main():
    data_analyser = DataAnalyser("data/sessions.jsonl", "data/products.jsonl", "data/users.jsonl")

    print("\n----------BASIC-MODEL-TRAINING-----------:")
    basic_model = Model(basic_dataset(data_analyser), best_params_search=False)
    basic_model.show_dataset_shapes()
    basic_model.train()
    print("\nBasic model testing on test data:")
    basic_model.test(show_accuracy=True, test_data=True)
    print("\nBasic model testing on train data:")
    basic_model.test(show_accuracy=True, test_data=False)

    joblib.dump(basic_model, 'models/basic_model')



    print("\n\n\n----------COMPLEX-MODEL-TRAINING-----------:")
    complex_model = Model(complex_dataset(data_analyser), best_params_search=True)
    complex_model.show_dataset_shapes()
    complex_model.train()
    print("\nComplex model testing on test data:")
    complex_model.test(show_accuracy=True, test_data=True)
    print("\nComplex model testing on train data:")
    complex_model.test(show_accuracy=True, test_data=False)

    joblib.dump(complex_model, 'models/complex_model')



    #data_analyser.show_sessions()
    #data_analyser.show_products()
    #data_analyser.show_users()

    #data_analyser.buy_sessions_statistics()
    #data_analyser.how_much_buy_sessions_without_view()
    #data_analyser.how_much_unknown_activities()
    
    #data_analyser.how_much_sessions_with_more_than_one_user()
    
    #data_analyser.how_much_null_users()
    #data_analyser.how_much_null_products()

    #data_analyser.how_much_incorrect_discounts()
    #data_analyser.how_much_incorrect_prices()
    #data_analyser.are_very_expensive_products_in_buy_sessions()
    #data_analyser.is_buy_activity_always_at_the_end_of_buy_session()

    # data_analyser.genders_proportion()

if __name__ == '__main__':
    main()