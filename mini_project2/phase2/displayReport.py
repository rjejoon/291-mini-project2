from pymongo import MongoClient

from bcolor.bcolor import bold
from bcolor.bcolor import cyan


def displayReport(db, uid: str) -> bool:
    '''
    Displays a report of the user if not signed in as anonymous.
    The user report includes:
        the # of questions owned and the average score for those questions, 
        the # of answers owned and the average score for those answers, and 
        the # of votes registered for the user
    
    Inputs:
        db -- pymongo.database.Database
        uid -- str
    Returns:
        bool
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
    '''
    Gets the # of questions the user owned and the average score for those questions 

    Inputs:
        posts -- pymongo.collection.Collection
        uid -- str
    Return:
        pymongo.command_cursor.CommandCursor
    '''
    
    return posts.aggregate([
                {"$match": {"$and": [{"OwnerUserId": uid}, 
                                     {"PostTypeId": "1"}]}},
                {"$group": {"_id": None, 
                            "count": {"$sum": 1},
                            "avgScore": {"$avg": "$Score"}}}
                ])


def getAInfo(posts, uid):
    '''
    Gets the # of answers the user owned and the average score for those answers

    Inputs:
        posts -- pymongo.collection.Collection
        uid -- str
    Return:
        pymongo.command_cursor.CommandCursor
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

def getVInfo(posts, uid):
    '''
    Gets the # of votes registered for the user

    Inputs:
        posts -- pymongo.collection.Collection
        uid -- str
    Return:
        pymongo.command_cursor.CommandCursor
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
