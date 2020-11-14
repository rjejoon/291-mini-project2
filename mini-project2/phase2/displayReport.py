from pymongo import MongoClient


def displayReport(db, uid: str) -> bool:

    if uid == '':
        # no report is displayed
        return False

    posts = db['posts']
    votes = db['votes']

    qInfo = posts.aggregate([
                {"$match": {"OwnerUserId": uid}},
                {"$match": {"PostTypeId": "1"}},
                {"$group": {"_id": None, 
                            "count": {"$sum": 1},
                            "avgScore": {"$avg": "$Score"}}}
                ])


    aInfo = posts.aggregate([
                {"$match": {"OwnerUserId": uid}},
                {"$match": {"PostTypeId": "2"}},
                {"$group": {"_id": None, 
                            "count": {"$sum": 1},
                            "avgScore": {"$avg": "$Score"}}}
                ])

    #TODO # of votes registered for the user    

    print(qInfo.next())
    print(aInfo.next())





