import json
import time
import os
import traceback
import asyncio
import subprocess, multiprocessing

import motor.motor_asyncio
from pymongo.collation import Collation

from phase1.extractTermsFrom import extractTermsFrom
from phase1.serializeDocumentsFrom import serializeDocumentsFrom
from bcolor.bcolor import green, warning, errmsg


async def main() -> int:
    '''
    Main structure of phase 1.
    '''
    try:
        start_time = time.time()
        port = getPort()
        client = motor.motor_asyncio.AsyncIOMotorClient(port=port)
        db = client['291db']

        # drop collections if already exist in db
        collList = ['posts', 'votes', 'tags']
        names = await db.list_collection_names()
        for col in collList:
            if col in names: 
                await db[col].drop()

        # collections
        posts = db['posts']

        st = time.time()
        postDocs = loadAllDocumentsFrom('Posts.json')
        print(green("Done!"))
        print("Loading and extracting took {:.5f} seconds.\n".format(time.time() - st))

        st = time.time()
        sub_insert_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'sub_insert.py')
        subprocess.Popen(['python3', sub_insert_path, str(port)])
        await insert_many_task(posts, postDocs)
        print("Insertions took {:.5f} seconds.\n".format(time.time() - st))

        print("Phase 1 complete!")
        print("It took {:.5f} seconds.".format(time.time() - start_time))

        return 0

    except TypeError as e:
        print(e)
        return 1

    except:
        print(traceback.print_exc())
        return 2

    finally:
        print("Disconnecting from MongoDB...")
        client.close()


async def insert_many_task(coll, documents):
    '''
    Asynchronous task that inserts all documents to the collection.
    '''
    print("Inserting documents to {}...".format(coll.name))
    await coll.insert_many(documents, ordered=False)
    documents.clear()
    print(green("Finished inserting {}!".format(coll.name)))
    if coll.name == 'posts':
        print("Creating index using terms...")
        await coll.create_index([('terms', 1)],
                                 collation=Collation(locale='en',
                                                     strength=2))    # for case=insensitive
        print(green("Finished creating the index!"))


def getPort() -> int:
    '''
    Prompts the user for MongoDB port and returns it.
    Raise TypeError if the user enters an invalid port.
    '''
    port = input("Enter MongoDB the port number: ")
    if port == '':
        return 27017    # default mongoDB port
    if not port.isdigit():
        raise TypeError("Invalid port number")

    return int(port)


def loadAllDocumentsFrom(f_name) -> list:
    '''
    Reads and serializes a json file and returns the list of MongoDB documents corresponding to each file.
    '''
    print("\nSearching and loading a json file...")
    desired_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')
    dirs_to_test = [desired_dir]
    # search from the root dir to 'data' (4 levels)
    for _ in range(3):
        desired_dir = os.path.dirname(desired_dir)
        dirs_to_test.append(desired_dir)

    dir_path = None
    for temp_dir in dirs_to_test:
        if os.path.isfile(os.path.join(temp_dir, f_name)):
            dir_path = temp_dir

    if dir_path is None:
        raise ValueError(errmsg("error: json file not found"))

    print(warning("Found a json file in {}".format(dir_path)))

    return serializeDocumentsFrom(dir_path, f_name)

	





