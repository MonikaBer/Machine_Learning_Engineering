import os
from DataAnalyser import DataAnalyser


def main():
    data_analyser = DataAnalyser("data/sessions.jsonl")
    #data_analyser.show_sessions()
    #data_analyser.buy_sessions_statistics()
    data_analyser.how_much_buy_sessions_without_view()


if __name__ == '__main__':
    main()
