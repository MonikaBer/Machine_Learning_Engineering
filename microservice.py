from Model import Model
import joblib


def main():
    complex_model = joblib.load('models/complex_model')

if __name__ == '__main__':
    main()