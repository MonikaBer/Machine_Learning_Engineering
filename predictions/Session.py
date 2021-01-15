

class Session:
    def __init__(self, session_id, activities, historical_users, historical_products, finished):
        self.session_id = session_id
        self.activities = []
        
        for a in activities:
            activity = SessionActivity(a)
            self.activities.append(activity)

        if not finished:
            self.if_buy = None
        elif activities[-1]['event_type'] == 'BUY_PRODUCT':
            self.if_buy = 1.0
        else:
            self.if_buy = 0.0

        self.user_id = None
        for a in self.activities:
            if a.user_id is not None:
                self.user_id = a.user_id
                break
        
        if self.user_id not in historical_users:
            self.user_id = None

        for a in self.activities:
            if_product_unknown = True
            for p in historical_products:
                if p.product_id == a.product_id:
                    if_product_unknown = False
                    break
            if if_product_unknown:
                a.product_id = None
        
        self.for_AB_exp = None


class SessionActivity:
    def __init__(self, activity):
        self.user_id = activity['user_id'] 
        self.product_id = activity['product_id']
