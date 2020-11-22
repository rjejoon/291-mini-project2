from pymongo import MongoClient

from bcolor.bcolor import bold
from bcolor.bcolor import cyan


def displayReport(db, uid: str) -> bool:
    '''
    Displays a report of the user if not signed in as anonymous.


    '''
    if uid == '':
        # no report is displayed
        return False

    qInfo = getQInfo(db['posts'], uid)
    aInfo = getAInfo(db['posts'], uid)
    vInfo = getVInfo(db['posts'], uid)

    print()
    header = cyan("Report for user: ") + uid
    print(header)
    print()

    # TODO What to print if the info is None?
    print(bold("   Questions"))
    for doc in qInfo:
        print("      Owned: {} avg score: {}".format(doc['count'], round(doc['avgScore'], 2)))

    print(bold("   Answers"))
    for doc in aInfo:
        print("      Owned: {}, avg score: {}".format(doc['count'], round(doc['avgScore'], 2)))

    print(bold("   Votes"))
    for doc in vInfo:
        print("      You got {} votes!".format(doc['count']))

    return True


def getQInfo(posts, uid):

    return posts.aggregate([
                {"$match": {"$and": [{"OwnerUserId": uid}, 
                                     {"PostTypeId": "1"}]}},
                {"$group": {"_id": None, 
                            "count": {"$sum": 1},
                            "avgScore": {"$avg": "$Score"}}}
                ])


def getAInfo(posts, uid):

    return posts.aggregate([
                {"$match": {"$and": [{"OwnerUserId": uid}, 
                                     {"PostTypeId": "2"}]}},
                {"$group": {"_id": None, 
                            "count": {"$sum": 1},
                            "avgScore": {"$avg": "$Score"}}},
                {"$project": { 
                                "count": { "$ifNull": [ "$count", 0 ]},
                                "avgScore": { "$ifNull": [ "$avgScore", 0]}
                             }}
                ])

def getVInfo(posts, uid):

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
