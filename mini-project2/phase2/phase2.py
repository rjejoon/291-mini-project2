import traceback

from pymongo import MongoClient

from phase1.phase1 import getPort
from bcolor.bcolor import errmsg
from phase2.displayReport import displayReport
from phase2.postQA import postQ, postAns
from phase2.searchQ import searchQ
from phase2.listAnswers import listAnswers
from phase2.votePost import votePost
from phase2.getValidInput import getValidInput 


def main():

    try:
        port = getPort()
        client = MongoClient(port=port)
        db = client['291db']
        uid = getUid()
        displayReport(db, uid)

        # TODO make a main loop of the program
        pressedExit = False
        while not pressedExit:
            printInterface()
            com = getValidInput("Enter a command: ", ['sq', 'pq', 'q'])

            if com == 'sq':
                targetQ, action = searchQ(db)
                if action == 'wa':
                    #postAns()
                    pass

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



def printInterface():
    pass

def getUid() -> str:
    '''
    Prompts the user for uid, which is a numeric field, and returns it.
    '''
    print("If you wish to sign in as anonymous, press enter without anything entered.")
    while True:
        uid = input('Enter your id: ')
        if uid == '':
            return '' 
        if uid.isdigit():
            return uid
        else:
            print("error: id must a number")


