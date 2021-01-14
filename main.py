from Model import Model
from DataAnalyser import DataAnalyser
from datasets import *
import os



def main():
    data_analyser = DataAnalyser("data/sessions.jsonl", "data/products.jsonl", "data/users.jsonl")

    model = Model(basic_dataset(data_analyser), best_params_search=True)
    model.show_dataset_shapes()
    model.train()
    print("\nTesting on test data:")
    model.test(show_accuracy=True, test_data=True)
    print("\nTesting on train data:")
    model.test(show_accuracy=True, test_data=False)


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
