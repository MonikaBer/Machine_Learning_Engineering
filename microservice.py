import joblib
from Model import Model


def main():
    basic_model = joblib.load('models/basic_model')
    complex_model = joblib.load('models/complex_model')

if __name__ == '__main__':
    main()