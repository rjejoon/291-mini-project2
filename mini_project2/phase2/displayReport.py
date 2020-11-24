from pymongo import MongoClient

from bcolor.bcolor import bold, cyan


def displayReport(db, uid: str) -> bool:
    '''
    Displays a report of the user if not signed in as anonymous.
    The user report includes:
        1. the # of questions owned and the average score for those questions, 
        2. the # of answers owned and the average score for those answers, and 
        3. the # of votes registered for the user
    
    Inputs:
        db -- Database
        uid -- str
    Returns:
        bool
    '''
    if uid == '':
        # no report is displayed
        return False

    qInfo = getQInfoQuery(db['posts'], uid)
    aInfo = getAInfoQuery(db['posts'], uid)
    vInfo = getVInfoQuery(db['posts'], uid)

    print()
    header = cyan("Report for user: ") + uid
    print(header)
    print()

    print(bold("   Questions"))
    exists = False
    for doc in qInfo:
        exists = True
        print("      Owned: {} avg score: {}".format(doc['count'], round(doc['avgScore'], 2)))
    if not exists:
        print("      N/A")

    print(bold("   Answers"))
    exists = False
    for doc in aInfo:
        exists = True
        print("      Owned: {} avg score: {}".format(doc['count'], round(doc['avgScore'], 2)))
    if not exists:
        print("      N/A")

    print(bold("   Votes"))
    exists = False
    for doc in vInfo:
        exists = True
        print("      You got {} votes!".format(doc['count']))
    if not exists:
        print("      N/A")

    return True


def getQInfoQuery(posts, uid):
    '''
    Gets the # of questions the user owned and the average score for those questions.

    Inputs:
        posts -- Collection
        uid -- str
    Return:
        CommandCursor
    '''
    
    return posts.aggregate([
                {"$match": {"$and": [{"OwnerUserId": uid}, 
                                     {"PostTypeId": "1"}]}},
                {"$group": {"_id": None, 
                            "count": {"$sum": 1},
                            "avgScore": {"$avg": "$Score"}}}
                ])


def getAInfoQuery(posts, uid):
    '''
    Gets the # of answers the user owned and the average score for those answers.

    Inputs:
        posts -- Collection
        uid -- str
    Return:
        CommandCursor
    '''
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


def getVInfoQuery(posts, uid):
    '''
    Gets the # of votes registered for the user.

    Inputs:
        posts -- Collection
        uid -- str
    Return:
        CommandCursor
    '''
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
