import traceback

from pymongo import MongoClient

from bcolor.bcolor import errmsg
from phase1.phase1 import getPort
from phase2.displayReport import displayReport
from phase2.postQ import postQ
from phase2.searchQ import searchQ
from phase2.listAnswers import listAnswers


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
            com = getValidInput("Enter a command: ", ['s', 'p', 'q'])

            if com == 's':
                targetQ, action = searchQ(db)
                if action == 'la':
                    listAnswers(db['posts'], targetQ)
            elif com == 'p':
                postQ(db, uid)
            elif com == 'q':
                pressedExit = True

        return 0

    except Exception as e:
        print(traceback.print_exc())
        return 1




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


def getValidInput(prompt: str, validEntries: list) -> str:

    while True:
        entry = input(prompt)
        if entry in validEntries:
            return entry
        print(errmsg("error: invalid entry"))
