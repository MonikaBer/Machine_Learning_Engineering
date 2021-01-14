from common.Session import EventType

class Event:
    def __init__(self, session_id, user_id, product_id, event_type):
        self.session_id = session_id
        self.user_id = user_id
        self.product_id = product_id
        if event_type == EventType.BUY:
            self.ifBuy = True
        else:
            self.ifBuy = False
