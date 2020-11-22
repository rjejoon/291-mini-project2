# import ijson.backends.yajl2 as ijson
import ijson
import time

from pymongo import MongoClient
from phase1.extractTermsFrom import extractTermsFrom


def main() -> int:

    st = time.time()
    client = MongoClient()
    db = client['291db']
    if 'posts' in db.list_collection_names():
        db['posts'].drop()

    posts = db['posts']
    with open('../Posts.json', 'r') as f:
        for doc in ijson.items(f, 'posts.row.item'):
            doc['terms'] = extractTermsFrom(doc)
            posts.insert_one(doc)


    print("It took {:.5f} seconds.".format(time.time() - st))


main()
