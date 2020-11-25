import json

from Session import Session

class DataAnalyser:

    def __init__(self, filename):    
        with open(filename, "r") as f:
            self.sessions = []

            lineDictList = []
            for line in f:
                lineDict = json.loads(line)
                lineDictList.append(lineDict)

        if len(lineDictList) == 0:
            return

        activities = []
        i = 0
        currSessionId = lineDictList[i]['session_id']
        activities.append(lineDictList[i])

        i = 1
        while i < len(lineDictList):
            if currSessionId == lineDictList[i]['session_id']:
                activities.append(lineDictList[i])
            else:
                session = Session(currSessionId, activities)
                self.sessions.append(session)
                activities = []
                currSessionId = lineDictList[i]['session_id']
                activities.append(lineDictList[i])
            i += 1

    def showSessions(self):
        for session in self.sessions:
            print("\nsessionId = {}:\n".format(session.sessionId))
            for sessionActivity in session.sessionActivities:
                print("timestamp = {}, userId = {}, productId = {}, eventType = {}, offeredDiscount = {}\n".format(sessionActivity.timestamp,
                                                                                                                sessionActivity.userId,
                                                                                                                sessionActivity.productId,
                                                                                                                sessionActivity.eventType,
                                                                                                                sessionActivity.offeredDiscount))

    def buySessionStatistics(self):
        buySessionsCount = 0
        for session in self.sessions:
            if session.ifBuy == True:
                buySessionsCount += 1

        print("TOTAL = {}, BUY_SESSIONS = {}, NOT_BUY_SESSIONS = {}"
                                            .format(len(self.sessions), buySessionsCount, len(self.sessions) - buySessionsCount))
