
from enum import Enum

class EventType(Enum):
    BUY = 0
    VIEW = 1
    UNKNOWN = 2

def get_enum_value_of_event_type(event_type):
    if event_type == 'BUY_PRODUCT':
        return EventType.BUY
    elif event_type == 'VIEW_PRODUCT':
        return EventType.VIEW
    else:
        return EventType.UNKNOWN


class Session:
    def __init__(self, session_id, activities):
        self.session_id = session_id
        self.session_activities = []
        self.if_buy = False

        for activity in activities:
            try:
                session_activity = SessionActivity(activity)
                self.session_activities.append(session_activity)
                if session_activity.event_type == EventType.BUY and self.if_buy == False:
                    self.if_buy = True
            except:
                print("Problem with data set formatting")
            
    def get_buy_session_activity(self):
        for session_activity in self.session_activities:
            if session_activity.event_type == EventType.BUY:
                return session_activity
        
        return None

    def get_view_activities_assoc_with_buy_activity(self, session_buy_activity):
        view_activities_assoc_with_buy_activity = []
        
        for session_activity in self.session_activities:
            if session_activity.event_type == EventType.VIEW and session_activity.product_id == session_buy_activity.product_id:
                view_activities_assoc_with_buy_activity.append(session_activity)

        return view_activities_assoc_with_buy_activity


class SessionActivity:
    def __init__(self, activity):
        self.timestamp = activity['timestamp']
        self.user_id = activity['user_id'] 
        self.product_id = activity['product_id']
        try:
            self.offered_discount = int(activity['offered_discount'])
        except:
            raise ValueError

        self.event_type = get_enum_value_of_event_type(activity['event_type'])
