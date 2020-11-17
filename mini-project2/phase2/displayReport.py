from pymongo import MongoClient


def displayReport(db, uid: str) -> bool:

    if uid == '':
        # no report is displayed
        return False

    posts = db['posts']
    votes = db['votes']

    qInfo = posts.aggregate([
                {"$match": {"$and": [{"OwnerUserId": uid}, 
                                     {"PostTypeId": "1"}]}},
                {"$group": {"_id": None, 
                            "count": {"$sum": 1},
                            "avgScore": {"$avg": "$Score"}}}
                ])


    aInfo = posts.aggregate([
                {"$match": {"$and": [{"OwnerUserId": uid}, 
                                     {"PostTypeId": "2"}]}},
                {"$group": {"_id": None, 
                            "count": {"$sum": 1},
                            "avgScore": {"$avg": "$Score"}}}
                ])

    vInfo = posts.aggregate([
                {"$match": {"OwnerUserId": uid}}, 
                {"$project": {"Id": 1, "OwnerUserId": 1}},
                {"$group": { "_id": {"OwnerUserId": "$OwnerUserId"}, "Ids": {"$push": "$Id"}}},
                {"$lookup": {
                                "from": "votes", 
                                "localField": "Ids", 
                                "foreignField": "PostId", 
                                "as": "vote_docs"
                            }},
                {"$project": {"count": {"$size": "$vote_docs"}}}
            ])

    for doc in qInfo:
        print(doc)
    for doc in aInfo:
        print(doc)
    for doc in vInfo:
        print(doc)





