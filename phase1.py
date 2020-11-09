from pymongo import MongoClient
import json
import time

def main():

    try:
        port = getPort()
        client = MongoClient()
        db = client['291db']

        # drop collections if already exist in db
        collList = ['posts', 'tags', 'votes']
        for col in collList:
            if col in db.list_collection_names():
                db[col].drop()

        posts = db['posts']
        tags = db['tags']
        votes = db['votes']

        postDocs = readDocsFrom('Posts.json')
        for postDoc in postDocs:
            postDoc['terms'] = extractTermsFrom(postDoc)

        tagsDocs = readDocsFrom('Tags.json')
        votesDocs = readDocsFrom('Votes.json')
        
        posts.insert_many(postDocs)
        tags.insert_many(tagsDocs)
        votes.insert_many(votesDocs)

        print("Phase 1 complete")

    except TypeError as e:
        print(e)

    except Exception as e:
        print(e)


def extractTermsFrom(postDoc):
    '''
    Extracts terms from the title and body if those fields exist in the given post document, 
    and returns them in a list.

    Input:
        postDoc -- dict
    Return:
        list
    '''
    title = []
    if 'Title' in postDoc:
        title = postDoc['Title'].split()
        title = map(termFilter, title)
        title = list(filter(lambda t: len(t)>=3, title))

    body = []
    if 'Body' in postDoc:
        body = postDoc['Body'].split()
        body = map(termFilter, body)
        body = list(filter(lambda t: len(t)>=3, body))

    return title + body
    

def termFilter(t: str) -> str:
    '''
    Filter out the whitespaces and punctuations from the string.
    '''

    t = t.strip()
    t = t.replace('<p>', '')
    t = t.replace('</p>', '')
    t = t.replace('.', '')
    t = t.replace(',', '')
    t = t.replace('?', '')
    t = t.replace('!', '')
    t = t.replace('.', '')
    t = t.replace(':', '')
    t = t.replace(';', '')
    t = t.replace('(', '')
    t = t.replace(')', '')
    t = t.replace('[', '')
    t = t.replace(']', '')
    t = t.replace('{', '')
    t = t.replace('}', '')
    t = t.replace('"', '')

    return t


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
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
