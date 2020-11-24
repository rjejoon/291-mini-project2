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

from bcolor.bcolor import errmsg, pink, underline, bold


def main() -> int:
    '''
    Main loop of the phase 2.
    '''
    try:
        port = getPort()
        client = MongoClient(port=port)
        db = client['291db']
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
                    postAns(db['posts'], uid, targetQ['Id'])
                elif action == 'vp' or (action == 'la' and listAnswers(db['posts'], targetQ)):
                    votePost(db['votes'], uid, targetQ['Id'])
                elif action == 'bm':
                    clear()
            elif command == 'pq':
                postQ(db, uid)
            else:
                pressedExit = True

        return 0

    except:
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


def getUid() -> str:
    '''
    Prompts the user for uid and returns it.
    The user can sign up as anonymous by inputting an empty string.
    '''
    print("Press enter without anything entered to sign in as anonymous.")
    return input('Enter your id: ')


def clear():
    '''
    Clears the shell.
    '''
    if os.name == 'nt':
        os.system('cls')
    elif os.name == 'posix':
        os.system('clear')
