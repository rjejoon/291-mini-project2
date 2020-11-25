import traceback
import os

from pymongo import MongoClient

from phase1.phase1 import getPort

from phase2.displayReport import displayReport
from phase2.postQA import postQ, postAns
from phase2.searchQ import searchQ
from phase2.listAnswers import listAnswers
from phase2.votePost import votePost
from phase2.getValidInput import getValidInput 
from phase2.clear import clear

from bcolor.bcolor import errmsg, pink, underline, bold


def main() -> int:
    '''
    Main loop of the phase 2.
    '''
    try:
        port = getPort()
        client = MongoClient(port=port)
        db = client['291db']
        maxIdDict = getMaxIds(db)
        clear()
        uid = getUid()
        displayReport(db, uid)

        pressedExit = False
        while not pressedExit:
            printInterface(uid)
            command = getValidInput("Enter a command: ", ['sq', 'pq', 'q'])

            if command == 'sq':
                targetQ, action = searchQ(db)
                if action == 'pa':
                    postAns(db['posts'], maxIdDict, uid, targetQ['Id'])
                elif action == 'vp':
                    votePost(db, maxIdDict, uid, targetQ['Id'])
                elif action == 'la':
                    targetAid = listAnswers(db['posts'], targetQ)
                    if targetAid != '':
                        votePost(db, maxIdDict, uid, targetAid)
                elif action == 'bm':
                    clear()
            elif command == 'pq':
                postQ(db, maxIdDict, uid)
            else:
                pressedExit = True

        return 0

    except TypeError as e:
        print(e)
        return 1

    except:
        print(traceback.print_exc())
        return 2

    finally:
        print("Disconnecting from MongoDB...")
        client.close()


def printInterface(uid):
    '''
    Displays a phase 2 main menu interface.
    '''
    if uid == '':
       uid = 'anonymous'

    header = "{}    User id: {}\n".format(pink('< M E N U >'), uid)
    pq = "{}ost a {}uestion".format(underline('P'), underline('Q'))
    sq = "{}earch {}uestions".format(underline('S'), underline('Q'))
    q = "{}uit".format(underline('Q'))

    print()
    print(header)
    print("  {}: {}".format(bold('pq'), pq))
    print("  {}: {}".format(bold('sq'), sq))
    print("  {}: {}".format(bold('q'), q))
    print()


def getMaxIds(db) -> dict:
    '''
    Gets current maximum Ids from posts, votes, tags collections.
    '''
    return { col: int(genID(db[col])) for col in ['posts', 'votes', 'tags'] }


def genID(collName) -> str:
    '''
    Finds the larget id in the given collection and generates a unique id

    Input: 
        collName -- pymongo.collection.Collection
    Return: 
        str
    '''
    cursor = collName.aggregate([
        {"$group": {"_id": None, "maxId": {"$max": {"$toInt": "$Id"}}}}
    ])
    maxId = 1
    for doc in cursor:
        maxId = doc['maxId']
    
    return str(int(maxId)+1)
    

def getUid() -> str:
    '''
    Prompts the user for uid and returns it.
    The user can sign up as anonymous by inputting an empty string.
    '''
    print("Press enter without anything entered to sign in as anonymous.")
    while True:
        uid = input('Enter your id: ')
        if uid == '':
            return ''
        if uid.isdigit():
            return uid
        print(errmsg("error: uid must be a number"))
