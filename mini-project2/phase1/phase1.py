from pymongo import MongoClient
import json
import time
import os
from phase1.extractTermsFrom import extractTermsFrom

def main() -> int:

    try:
        start_time = time.time()
        port = getPort()
        client = MongoClient(port=port)
        db = client['291db']

        # drop collections if already exist in db
        collList = ['posts', 'tags', 'votes']
        for col in collList:
            if col in db.list_collection_names():
                db[col].drop()

        posts = db['posts']
        tags = db['tags']
        votes = db['votes']

        print("Inserting documents to posts collection...")
        postDocs = readDocumentsFrom('Posts.json')
        for postDoc in postDocs:
            postDoc['terms'] = extractTermsFrom(postDoc)
        posts.insert_many(postDocs)
        print("Done!\n")

        print("Inserting documents to tags collection...")
        tagsDocs = readDocumentsFrom('Tags.json')
        tags.insert_many(tagsDocs)
        print("Done!\n")

        print("Inserting documents to votes collection...")
        votesDocs = readDocumentsFrom('Votes.json')
        votes.insert_many(votesDocs)
        print("Done!\n")

        print("Phase 1 complete!")
        print("It took {:.5f} seconds".format(time.time() - start_time))

        return 0

    except TypeError as e:
        print(e)
        return 1

    except Exception as e:
        print(e)
        return 2


def getPort() -> int:
    '''
    Prompts the user for MongoDB port number and returns it.
    Raise TypeError if the user enters an invalid port number.
    '''
    port = input("Enter MongoDB the port number: ")
    if port == '':
        return 27017    # default mongoDB port
    if not port.isdigit():
        raise TypeError("Invalid port number")

    return int(port)


def readDocumentsFrom(filename: str) -> list:
    '''
    Reads a specified json file and returns the list of documents.
    '''
    fpath = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', filename)
    collName = filename[:-5].lower()
    with open(fpath, 'r') as f:
        data = json.load(f)

    return data[collName]['row'] 





