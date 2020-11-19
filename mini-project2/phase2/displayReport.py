from pymongo import MongoClient

from bcolor.bcolor import bold
from bcolor.bcolor import cyan


def displayReport(db, uid: str) -> bool:

    if uid == '':
        # no report is displayed
        return False

    qInfo = getQInfo(db['posts'])
    aInfo = getAInfo(db['posts'])
    vInfo = getVInfo(db['votes'])

    print()
    header = cyan("Report for user: ") + uid
    print(header)
    print()

    print(bold("Questions"))
    for doc in qInfo:
        print("   Owned: {} avg score: {}".format(doc['count'], doc['avgScore']))

    print(bold("Answers"))
    for doc in aInfo:
        print("   Owned: {}, avg score: {}".format(doc['count'], doc['avgScore']))

    print(bold("Votes"))
    for doc in vInfo:
        print("   You got {} votes!".format(doc['count']))
    print()

    return True


def getQInfo(posts):

    return posts.aggregate([
                {"$match": {"$and": [{"OwnerUserId": uid}, 
                                     {"PostTypeId": "1"}]}},
                {"$group": {"_id": None, 
                            "count": {"$sum": 1},
                            "avgScore": {"$avg": "$Score"}}}
                ])


def getAInfo(posts):

    return posts.aggregate([
                {"$match": {"$and": [{"OwnerUserId": uid}, 
                                     {"PostTypeId": "2"}]}},
                {"$group": {"_id": None, 
                            "count": {"$sum": 1},
                            "avgScore": {"$avg": "$Score"}}}
                ])

def getVInfo(votes):

    return posts.aggregate([
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
