from DataAnalyser import DataAnalyser
import numpy as np

from User import Gender


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
                        get_previous_buy_sessions_for_user_proportion(s, data_analyser),
                        #find_price_reduction(s, data_analyser),
                        #get_user_gender(s, data_analyser),
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


def get_user_gender(session, data_analyser:DataAnalyser):
    """ Płeć użytkownika """
    for a in session.session_activities:
        for u in data_analyser.users:
            if a.user_id == u.user_id:
                if u.gender == Gender.MALE:
                    return int(Gender.MALE)
                elif u.gender == Gender.FEMALE:
                    return int(Gender.FEMALE)
                break
    return int(Gender.UNKNOWN)
                

def get_previous_buy_sessions_for_user_proportion(s, data_analyser:DataAnalyser):
    """ Stosunek dotychczasowych sesji użytkownika zakończonych zakupem """
    buy_counter = 0
    total_counter = 0
    user_id = get_session_user_id(s, data_analyser)
    print(user_id)

    if user_id != -1:
        for session in data_analyser.sessions:
            user_id2 = get_session_user_id(session, data_analyser)
            
            if user_id == user_id2:
                if session.if_buy:
                    buy_counter += 1
                total_counter += 1
                
            if session.session_id == s.session_id:
                if total_counter == 0:
                    return 0
                return buy_counter / total_counter * 100

    if total_counter == 0:
        return 0
    return buy_counter / total_counter * 100

def get_session_user_id(session, data_analyser:DataAnalyser):
    for a in session.session_activities:
        if a.user_id != None:
            return a.user_id
    return -1


