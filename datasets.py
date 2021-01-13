from DataAnalyser import DataAnalyser
import numpy as np


def basic_dataset(data_analyser:DataAnalyser):
    """
    Atrybuty:
    1) Ilość aktywności w sesji                             - bardzo dużo informacji wnosi
    2) Obniżka cenowa ostanio ogladanego produktu           - nie wnosi nic
    3) Zniżka ostatniej aktywnosci                          - nie wnosi nic
    4) Czas trwania w sekundach                             - trochę informacji wnosi względem samych zer, ale i tak 1) lepsze samo
    5) Częstotliwość kupowania ostatnio oglądanego produktu - prawie nic nie wnosi
    """
    # W tupli wszystkie features, które model będzie uwzględniał
    features = np.array([(
                        len(s.session_activities),
                        find_price_reduction(s, data_analyser),
                        # s.session_activities[-1].offered_discount,
                        # s.duration,
                        find_frequency(s, data_analyser),
                        # 0,
                        ) 
                        for s in data_analyser.sessions])

    labels  = np.array([int(s.if_buy) for s in data_analyser.sessions])

    return features, labels


def find_price_reduction(session, data_analyzer:DataAnalyser):
    """ Obniżka cenowa ostatnio oglądanego produktu: zniżka * cena """
    last_product_id = session.session_activities[-1].product_id
    for p in data_analyzer.products:
        if p.product_id == last_product_id:
            return p.price * session.session_activities[-1].offered_discount
    return 0    # nie znaleziono produktu


def find_frequency(session, data_analyzer:DataAnalyser):
    """ Częstotliwość kupowania ostatnio oglądanego produktu """
    last_product_id = session.session_activities[-1].product_id
    for p in data_analyzer.products:
        if p.product_id == last_product_id:
            return p.frequency
    return 0    # nie znaleziono produktu