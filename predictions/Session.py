class Session:
    def __init__(self, first_event):
        self.events = []
        self.events.append(first_event)
        self.session_id = first_event.session_id
        
        self.user_id = None
        if first_event.user_id is not None:
            self.user_id = first_event.user_id

    def addEvent(self, event):
        self.events.append(event)
