import numpy as np

from DataAnalyser import DataAnalyser
from User import Gender


def basic_dataset(data_analyser:DataAnalyser):
    """
    Atrybut:
    1)Ilość aktywności w sesji
    """

    features = np.array([(
        len(s.session_activities),
        ) 
        for s in data_analyser.sessions])
    
    labels  = np.array([int(s.if_buy) for s in data_analyser.sessions])

    return features, labels




def complex_dataset(data_analyser:DataAnalyser):
    """
    Atrybuty:
    1) Ilość aktywności w sesji                                                                         - bardzo dużo informacji wnosi
    2) Stosunek sesji zakończonych kupnem do wszystkich dotychczasowych sesji usera                     - trochę informacji wnosi
    3) Częstotliwość kupowania ostatnio oglądanego produktu                                             - trochę informacji wnosi                
    
    4) Atrakcyjność cenowa (cena ostatnio oglądanego produktu w sesji wzg śr ceny produktów z tej kat.) - nic nie wnosi
    5) Kategoria produktu                                                                               - prawie nic nie wnosi 
    6) Obniżka cenowa ostanio ogladanego produktu                                                       - nie wnosi nic
    7) Zniżka ostatniej aktywnosci                                                                      - nie wnosi nic
    8) Czas trwania sesji w sekundach                                                                   - trochę informacji wnosi względem samych zer, ale i tak 1) lepsze samo
    9) Miasto użytkownika związanego z sesją                                                            - nie wnosi nic
    10) Płeć użytkownika związanego z sesją                                                             - nie wnosi nic
    """
    # W tupli wszystkie features, które model będzie uwzględniał
    features = np.array([(
                        len(s.session_activities),
                        get_previous_buy_sessions_for_user_proportion(s, data_analyser),
                        find_frequency(s, data_analyser),

                        #get_price_attractiveness(s, data_analyser),
                        #get_category(s, data_analyser),
                        # find_price_reduction(s, data_analyser),
                        # s.session_activities[-1].offered_discount,
                        # s.duration,
                        # get_city(s, data_analyser),
                        # get_user_gender(s, data_analyser),
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
    for u in data_analyser.users:
        if session.user_id == u.user_id:
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

    if s is not None:
        for session in data_analyser.sessions:
            if s.user_id == session.user_id:
                if session.if_buy:
                    buy_counter += 1
                total_counter += 1
                
            if session.session_id == s.session_id:
                if total_counter == 0:
                    return 0
                return buy_counter / total_counter

    if total_counter == 0:
        return 0
    return buy_counter / total_counter

def get_price_attractiveness(s, data_analyser:DataAnalyser):
    """ Cena ostatnio oglądanego produktu w sesji podzielona przez średnią cenę wszystkich produktów z tej podkategorii """
    last_product_id = s.session_activities[-1].product_id
    last_product_category = None

    for p in data_analyser.products:
        if p.product_id == last_product_id:
            last_product_category = p.category_path
            last_product_price = p.price

    if last_product_category is None or last_product_price is None:
        return 0

    prices_sum_in_category = 0
    counter = 0
    for p in data_analyser.products:
        if p.category_path == last_product_category:
            prices_sum_in_category += p.price
            counter += 1

    avg_price_in_category = round(prices_sum_in_category / counter, 2)
    return last_product_price / avg_price_in_category

def get_city(s, data_analyser:DataAnalyser):
    for u in data_analyser.users:
        if u.user_id == s.user_id:
            ind = 0
            for city in data_analyser.cities_set:
                if city == u.city:
                    return ind
                ind += 1
    return 0

def get_category(s, data_analyser:DataAnalyser):
    last_product_id = s.session_activities[-1].product_id
    last_product_category = None
    
    for p in data_analyser.products:
        if p.product_id == last_product_id:
            last_product_category = p.category_path
            ind = 0
            for c in data_analyser.categories_set:
                if c == p.category_path:
                    return ind
                ind += 1

    return -1
