import joblib
from common.Model import Model
from predictions.HistoricalData import HistoricalData
from predictions.ComplexPredictiveModule import ComplexPredictiveModule


def main():
    historical_data = HistoricalData("data/products.jsonl", "data/users.jsonl", "data/sessions.jsonl")
    
    # basic_model = joblib.load('models/basic_model')
    complex_model = joblib.load('models/complex_model')

    print('----------PREDICTIONS-SERVING----------')
    
    complex_pred_mod = ComplexPredictiveModule(complex_model, historical_data)
    complex_pred_mod.load_input_data('data/current_sessions.jsonl')
    complex_pred_mod.build_features()
    complex_pred_mod.predict()
    complex_pred_mod.show_result()


if __name__ == '__main__':
    main()
