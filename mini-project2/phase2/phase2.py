from pymongo import MongoClient

from phase1.phase1 import getPort
from phase2.displayReport import displayReport



def main():

    try:
        port = getPort()
        client = MongoClient(port=port)
        db = client['291db']

        # collections
        posts = db['posts']
        tags = db['tags']
        votes = db['votes']

        uid = getUid()
        displayReport(uid)

        return 0

    except Exception as e:
        print(e)
        return 1




def getUid() -> int:
    '''
    Prompts the user for uid, which is a numeric field, and returns it.
    '''
    print("If you wish to sign in as anonymous, press enter without anything entered.")
    while True:
        uid = input('Enter your id: ')
        if uid == '':
            return -1
        if uid.isdigit():
            return int(uid)
        else:
            print("error: id must a number")
