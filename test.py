import os
import sys
import json
import asyncio

import motor.motor_asyncio


async def main():
    port = int(sys.argv[1])
    client = motor.motor_asyncio.AsyncIOMotorClient(port=port)
    db = client['291db']

    dir_path = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(dir_path, "Votes.json"), 'r') as f:
        voteDocs = json.load(f)["votes"]['row']

    with open(os.path.join(dir_path, "Tags.json"), 'r') as f:
        tagDocs = json.load(f)["tags"]['row']

    await asyncio.gather(
            insert_many_task(db['votes'], voteDocs),
            insert_many_task(db['tags'], tagDocs),
    )


async def insert_many_task(coll, documents): 
    '''
    Asynchronous task that inserts all documents to the collection.
    '''
    print("Inserting documents to {}...".format(coll.name))
    await coll.insert_many(documents, ordered=False)
    documents.clear()
    print(green("Finished inserting {}!".format(coll.name)))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

