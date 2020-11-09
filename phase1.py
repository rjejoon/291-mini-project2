from pymongo import MongoClient
import json


def main():

    try:
        port = getPort()
        client = MongoClient()
        db = client['291db']

        # drop collections if exist in db
        collList = ['posts', 'tags', 'votes']
        for col in collList:
            if col in db.list_collection_names():
                db[col].drop()

        posts = db['posts']
        tags = db['tags']
        votes = db['votes']

        postDocs = readDocsFrom('Posts.json')
        tagsDocs = readDocsFrom('Tags.json')
        votesDocs = readDocsFrom('Votes.json')
        
        posts.insert_many(postRows)
        tags.insert_many(tagsRows)
        votes.insert_many(votesRows)

    except TypeError as e:
        print(e)

    except Exception as e:
        print(e)


def getPort():
    '''
    Prompts the user for MongoDB port number and returns it.
    Raise TypeError if the user enters an invalid port number.
    '''
    port = input("Enter MongoDB the port number: ")
    if not port.isdigit():
        raise TypeError("Invalid port number")

    return int(port)


def readDocsFrom(filename):
    '''
    Reads a specified json file and returns the list of documents.

    Input:
        filename -- str
    Return:
        list
    '''
    collName = filename[:-5].lower()
    with open(filename, 'r') as f:
        data = json.load(f)

    return data[collName]['row'] 



if __name__ == "__main__":
    main()
