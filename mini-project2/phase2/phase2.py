from pymongo import MongoClient

from phase1.phase1 import getPort
from phase2.displayReport import displayReport
from phase2.postQ import postQ
from phase2.searchQ import searchQ



def main():

    try:
        port = getPort()
        client = MongoClient(port=port)
        db = client['291db']

        uid = getUid()
        displayReport(db, uid)

        #postQ(db, uid)
        searchQ(db)

        return 0

    except Exception as e:
        print(e)
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
