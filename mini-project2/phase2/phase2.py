import traceback
import os

from pymongo import MongoClient

from phase1.phase1 import getPort
from bcolor.bcolor import errmsg
from bcolor.bcolor import pink
from bcolor.bcolor import underline
from bcolor.bcolor import bold 
from phase2.displayReport import displayReport
from phase2.postQA import postQ, postAns
from phase2.searchQ import searchQ
from phase2.listAnswers import listAnswers
from phase2.votePost import votePost
from phase2.getValidInput import getValidInput 


def main() -> int:
    '''
    Main loop of the program.
    '''
    try:
        port = getPort()
        client = MongoClient(port=port)
        db = client['291db']
        uid = getUid()
        displayReport(db, uid)

        os.system('clear')
        pressedExit = False
        while not pressedExit:
            printInterface(uid)
            com = getValidInput("Enter a command: ", ['sq', 'pq', 'q'])

            if com == 'sq':
                targetQ, action = searchQ(db)

                if action == 'pa':
                    postAns(db, uid, targetQ['_id'])
                elif action == 'vp' or (action == 'la' and listAnswers(db['posts'], targetQ)):
                    votePost()
                    
            elif com == 'pq':
                postQ(db, uid)
            else:
                pressedExit = True

        return 0

    except Exception as e:
        print(traceback.print_exc())
        return 1

    finally:
        print("Disconnecting from MongoDB...")
        client.close()


def printInterface(uid):
    '''
    Displays a phase 2 main menu interface.
    '''
    if uid == '':
        uid = 'anonymous'

    header = "{}    Signed in as: {}\n".format(pink('< M E N U >'), uid)
    pq = "{}ost a {}uestion".format(underline('P'), underline('Q'))
    sq = "{}earch {}uestions".format(underline('S'), underline('Q'))
    q = "{}uit".format(underline('Q'))

    print(header)
    print("  {}: {}".format(bold('pq'), pq))
    print("  {}: {}".format(bold('sq'), sq))
    print("  {}: {}".format(bold('q'), q))
    print()


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
        else:
            print(errmsg("error: id must a number"))


