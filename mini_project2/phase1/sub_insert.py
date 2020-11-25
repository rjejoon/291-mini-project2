import os
import sys
import json
import asyncio
import traceback

import motor.motor_asyncio

from phase1.serializeDocumentsFrom import serializeDocumentsFrom


async def main():
    try:
        port = int(sys.argv[1])
        client = motor.motor_asyncio.AsyncIOMotorClient(port=port)
        db = client['291db']
        voteDocs, tagDocs = loadAllDocumentsFrom('Votes.json', 'Tags.json')

        await asyncio.gather(
                insert_many_task(db['votes'], voteDocs),
                insert_many_task(db['tags'], tagDocs),
        )

        return 0

    except:
        print(traceback.print_exc())
        return 2


async def insert_many_task(coll, documents): 
    '''
    Asynchronous task that inserts all documents to the collection.
    '''
    print("Inserting documents to {}...".format(coll.name))
    await coll.insert_many(documents, ordered=False)
    documents.clear()
    print("Finished inserting {}!".format(coll.name))


def loadAllDocumentsFrom(*args) -> list:
    '''
    Reads and serializes json files and returns the list of MongoDB documents corresponding to each file.
    '''
    print("\nSearching and loading two json files...")
    desired_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')
    dirs_to_test = [desired_dir]
    # search from the root dir to 'data' (4 levels)
    for _ in range(3):
        desired_dir = os.path.dirname(desired_dir)
        dirs_to_test.append(desired_dir)

    dir_path = None
    for temp_dir in dirs_to_test:
        if jsonFilesExistIn(temp_dir, args):
            dir_path = temp_dir
    print(warning("Found {} json files in {}".format(len(args), dir_path)))

    return [serializeDocumentsFrom(dir_path, f_name) for f_name in args]

	
def jsonFilesExistIn(dir_path, filenames) -> bool:
    '''
    Returns True if all the files in filenames exist in the dir_path.
    '''
    return all((os.path.isfile(os.path.join(dir_path, f_name)) for f_name in filenames))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

