import joblib
import json
import sys
from common.Model import Model
from predictions.HistoricalData import HistoricalData
from predictions.ComplexPredictiveModule import ComplexPredictiveModule
from predictions.BasicPredictiveModule import BasicPredictiveModule
from predictions.Session import Session


def load_input_data(input_filename, historical_users, historical_products):
    open_sessions = []

    with open(input_filename, 'r') as f:
        line_dict_list = []
        for line in f:
            line_dict = json.loads(line)
            line_dict_list.append(line_dict)

    if len(line_dict_list) == 0:
        return open_sessions

    activities = []
    i = 0
    curr_session_id = line_dict_list[i]['session_id']
    activities.append(line_dict_list[i])

    print(f'{line_dict_list[i]}\n')

    i = 1
    while i < len(line_dict_list):
        print(f'{line_dict_list[i]}\n')
        if curr_session_id == line_dict_list[i]['session_id']:
            activities.append(line_dict_list[i])
        else:
            session = Session(curr_session_id, activities, historical_users, historical_products, finished=False)
            open_sessions.append(session)
            activities = []
            curr_session_id = line_dict_list[i]['session_id']
            activities.append(line_dict_list[i])
        i += 1
    
    if len(activities) != 0:
        session = Session(curr_session_id, activities, historical_users, historical_products, finished=False)
        open_sessions.append(session)
    
    return open_sessions


def divide_open_sessions(open_sessions):
    set_for_complex = []
    set_for_basic = []
    
    for s in open_sessions:
        if s.user_id is None:
            continue
        elif s.user_id % 2 == 0:
            set_for_basic.append(s)
        else:
            set_for_complex.append(s)

    return set_for_complex, set_for_basic


def main():
    if len(sys.argv) != 3 or sys.argv[1] == "help":
        print(  "Usage: python3 microservice.py --mode <mode>\n" +
                "Mode: basic / complex / ab" )
        exit(1)

    mode = sys.argv[2]
    
    historical_data = HistoricalData("data/products.jsonl", "data/users.jsonl", "data/sessions.jsonl")
    open_sessions = load_input_data('data/current_sessions.jsonl', historical_data.users, historical_data.products)

    
    if mode == 'ab':
        print('\n----------A/B-EXP-PREDICTIONS-SERVING----------\n')

        complex_model = joblib.load('models/complex_model')
        complex_pred_mod = ComplexPredictiveModule(complex_model, historical_data)
        basic_model = joblib.load('models/basic_model')
        basic_pred_mod = BasicPredictiveModule(basic_model)
        
        set_for_complex, set_for_basic = divide_open_sessions(open_sessions)
        complex_pred_mod.load_data(set_for_complex)
        basic_pred_mod.load_data(set_for_basic)

        complex_pred_mod.build_features()
        complex_pred_mod.predict()
        basic_pred_mod.predict()
        
        complex_pred_mod.show_result()
        basic_pred_mod.show_result()

        complex_pred_mod.save_result('results/complex_result')
        basic_pred_mod.save_result('results/basic_result')

    elif mode == 'basic':
        print('\n----------BASIC-MODEL-PREDICTIONS-SERVING----------\n')

        basic_model = joblib.load('models/basic_model')
        basic_pred_mod = BasicPredictiveModule(basic_model)

        basic_pred_mod.load_data(open_sessions)

        basic_pred_mod.predict()

        basic_pred_mod.show_result()

    elif mode == 'complex':
        print('\n----------COMPLEX-MODEL-PREDICTIONS-SERVING----------\n')

        complex_model = joblib.load('models/complex_model')
        complex_pred_mod = ComplexPredictiveModule(complex_model, historical_data)

        complex_pred_mod.load_data(open_sessions)

        complex_pred_mod.build_features()
        complex_pred_mod.predict()
        complex_pred_mod.show_result()

    else:
        print(  'Unknown mode\n' +
                "Usage: python3 microservice.py <mode>\n" +
                "Mode: basic / complex / ab" )
        exit(1)

if __name__ == '__main__':
    main()
