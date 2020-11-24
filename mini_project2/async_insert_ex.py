from pymongo import MongoClient
from pymongo.write_concern import WriteConcern as wc
import json
import time


def main():

    client = MongoClient()
    db = client['291db']
    posts = db['posts']

    if 'posts' in db.list_collection_names():
        db['posts'].drop()

    with open('../Posts.json', 'r') as f:
        postDocs = json.load(f)['posts']['row']

    st = time.time()
    for postDoc in postDocs:
        posts.insert_one(postDoc, bypass_document_validation=True)
    print(time.time() - st, '\n')

    db['posts'].drop()

    st = time.time()
    for postDoc in postDocs:
        posts.insert_one(postDoc)
    print(time.time() - st)


main()

