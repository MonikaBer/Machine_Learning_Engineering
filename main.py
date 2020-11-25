import os
from DataAnalyser import DataAnalyser


def main():
    dataAnalyser = DataAnalyser("data/sessions.jsonl")
    #dataAnalyser.showSessions()
    dataAnalyser.buySessionStatistics()
    


if __name__ == "__main__":
    main()
