import json

from Session import Session
from Session import EventType

class DataAnalyser:

    def __init__(self, filename):    
        with open(filename, 'r') as f:
            self.sessions = []

            line_dict_list = []
            for line in f:
                line_dict = json.loads(line)
                line_dict_list.append(line_dict)

        if len(line_dict_list) == 0:
            return

        activities = []
        i = 0
        curr_session_id = line_dict_list[i]['session_id']
        activities.append(line_dict_list[i])

        i = 1
        while i < len(line_dict_list):
            if curr_session_id == line_dict_list[i]['session_id']:
                activities.append(line_dict_list[i])
            else:
                session = Session(curr_session_id, activities)
                self.sessions.append(session)
                activities = []
                curr_session_id = line_dict_list[i]['session_id']
                activities.append(line_dict_list[i])
            i += 1

    def show_sessions(self):
        for session in self.sessions:
            print("\nsession id = {}:\n".format(session.session_id))
            for session_activity in session.session_activities:
                print("timestamp = {}, user id = {}, product id = {}, event type = {}, offered discount = {}\n".format(session_activity.timestamp,
                                                                                                                session_activity.user_id,
                                                                                                                session_activity.product_id,
                                                                                                                session_activity.event_type,
                                                                                                                session_activity.offered_discount))

    # statistics of BUY and NOT BUY sessions
    def buy_sessions_statistics(self):
        buy_sessions_count = 0
        for session in self.sessions:
            if session.if_buy == True:
                buy_sessions_count += 1

        print("TOTAL = {}, BUY SESSIONS = {}, NOT BUY SESSIONS = {}"
                                            .format(len(self.sessions), buy_sessions_count, len(self.sessions) - buy_sessions_count))

    # check in each BUY SESSION that VIEW precedes BUY
    def how_much_buy_sessions_without_view(self):
        buy_sessions_without_view_count = 0
        
        for session in self.sessions:
            if session.if_buy:
                buy_activity = session.get_buy_session_activity()
                view_activities_assoc_with_buy_activity = session.get_view_activities_assoc_with_buy_activity(buy_activity) 

                if len(view_activities_assoc_with_buy_activity) == 0:
                    buy_sessions_without_view_count += 1

        print ("Number of BUY sessions without VIEW events = {}".format(buy_sessions_without_view_count))