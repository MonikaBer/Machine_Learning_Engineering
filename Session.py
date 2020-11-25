
class Session:
    def __init__(self, sessionId, activities):
        self.sessionId = sessionId
        self.sessionActivities = []
        self.ifBuy = False

        for activity in activities:
            sessionActivity = SessionActivity(activity)
            self.sessionActivities.append(sessionActivity)
            if sessionActivity.eventType == "BUY_PRODUCT" and self.ifBuy == False:
                self.ifBuy = True

class SessionActivity:
    def __init__(self, activity):
        self.timestamp = activity['timestamp']
        self.userId = activity['user_id']
        self.productId = activity['product_id']
        self.eventType = activity['event_type']
        self.offeredDiscount = activity['offered_discount']
