import json
import joblib
import numpy as np
from common.Model import Model
from predictions.SystemData import SystemData
from predictions.Event import Event


def parse_event(event_line):
    event = Event(  event_line['session_id'], event_line['user_id'], 
                            event_line['product_id'], event_line['event_type'])
    return event


def show_event(event, only_session_id):
    if only_session_id:
        print (f'\nsession_id = {event.session_id}\n')
        return
    
    print ( f'\nsession id = {event.session_id}, user id = {event.user_id}, ' + 
            f'product id = {event.product_id}, zakup = {event.ifBuy}\n')


def build_features_for_complex_model(event, system_data):
    features = np.array([(
                        system_data.get_session_length(event),
                        system_data.get_previous_buy_sessions_for_user_proportion(event),
                        system_data.get_buying_frequency(event),
                        )
                        for a in range(0,2)])

    return features


def main():
    system_data = SystemData("data/products.jsonl", "data/users.jsonl")
    
    # basic_model = joblib.load('models/basic_model')
    complex_model = joblib.load('models/complex_model')

    print('----------PREDICTIONS-SERVING----------')
    
    events_number = 0
    correct_preds = 0
    with open("data/current_sessions.jsonl", 'r') as f:
            for line in f:
                event_line = json.loads(line)
                event = parse_event(event_line)
                show_event(event, only_session_id=True)

                system_data.put_event_to_history(event)

                features = build_features_for_complex_model(event, system_data)

                result = complex_model.predict(features)
                if result == event.ifBuy:
                    correct_preds += 1
                events_number += 1
                accuracy = round(correct_preds / events_number * 100, 2)
                print(f'Accuracy {accuracy}\n')


if __name__ == '__main__':
    main()
