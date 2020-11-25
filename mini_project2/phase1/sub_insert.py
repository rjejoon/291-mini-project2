import os
import sys
import json
import asyncio
import traceback

import motor.motor_asyncio

OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'


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
    print(green("Finished inserting {}!".format(coll.name)))


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

    if dir_path is None:
        raise ValueError(errmsg("error: json file not found"))

    print(warning("Found {} json files in {}".format(len(args), dir_path)))

    return [serializeDocumentsFrom(dir_path, f_name) for f_name in args]

	
def jsonFilesExistIn(dir_path, filenames) -> bool:
    '''
    Returns True if all the files in filenames exist in the dir_path.
    '''
    return all((os.path.isfile(os.path.join(dir_path, f_name)) for f_name in filenames))


def serializeDocumentsFrom(dir_path, f_name):
    '''
    Loads and serializes a json file.
    Returns the data in a list.
    '''
    collName = f_name[:-5].lower()
    print("Loading {}...".format(f_name))
    with open(os.path.join(dir_path, f_name), 'r') as f:
        docs = json.load(f)[collName]['row']

    return docs


def warning(s):
    return WARNING + s + ENDC

def green(s):
    return OKGREEN + s + ENDC

def errmsg(s):
    return FAIL + s + ENDC



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

