import json
import ijson
import time
import os
import traceback
import asyncio
# import aiofiles
from async_generator import async_generator, yield_, aclosing

import motor.motor_asyncio

from phase1.extractTermsFrom import extractTermsFrom
from bcolor.bcolor import green, warning


async def main() -> int:

    try:
        start_time = time.time()
        port = getPort()
        client = motor.motor_asyncio.AsyncIOMotorClient(port=port)
        db = client['291db']
        loop = asyncio.get_event_loop()
        collList = ['posts', 'votes', 'tags']
        names = await db.list_collection_names()
        for col in collList:
            if col in names: 
                await db[col].drop()

        # drop collections if already exist in db
        collList = ['posts', 'tags', 'votes']

        posts = db['posts']
        tags = db['tags']
        votes = db['votes']

        # TODO reduce insertion time. current : 120 sec
        print("\nSearching and loading three json files...")
        st = time.time()
        dir_path = getDirPath('Posts.json', 'Tags.json', 'Votes.json')

        with open(os.path.join(dir_path, 'Posts.json'), 'r') as f:
            postDocs = json.load(f)['posts']['row']
        with open(os.path.join(dir_path, 'Votes.json'), 'r') as f:
            voteDocs = json.load(f)['votes']['row']
        with open(os.path.join(dir_path, 'Tags.json'), 'r') as f:
            tagDocs = json.load(f)['tags']['row']

        print(green("Done!"))
        print("Loading took {:.5f} seconds.\n".format(time.time() - st))


        await asyncio.gather(extractTerms(posts, dir_path), insert(votes, voteDocs), insert(tags, tagDocs))
        
        # posts.insert_many(postDocs, ordered=False)
        # votes.insert_many(voteDocs, ordered=False)
        # tags.insert_many(tagDocs, ordered=False)
        print(green("Done!"))
        print("Insertion took {:.5f} seconds.\n".format(time.time() - st))
        return

        st = time.time()
        print("Creating index using terms...")
        posts.create_index([('terms', 1)],
                            collation=Collation(locale='en',
                                                strength=2))    # for case=insensitive
        print(green("Done!"))
        print("Indexing took {:.5f} seconds.\n".format(time.time() - st))

        print("Phase 1 complete!")
        print("It took {:.5f} seconds.".format(time.time() - start_time))

        return 0

    except TypeError as e:
        print(traceback.print_exc())
        return 1

    except:
        print(traceback.print_exc())
        return 2

    finally:
        print("Disconnecting from MongoDB...")
        client.close()


async def extractTerms(postColl, postDocs):

    print("Extracting terms from posts documents...")
    st = time.time()

    async for postDoc in loadPostDocs(postDocs):
        await extractTermsFrom(postDoc)

            # await postColl.insert_one(postDoc)

    print(green("Done!"))
    print("Extracting terms took {:.5f} seconds.\n".format(time.time() - st))


@async_generator
async def loadPostDocs(postDocs):

    async for postDoc in postDocs:
        await _yield(postDoc)
     
    # f_path = os.path.join(dir_path, 'Posts.json')
    # async with aiofiles.open(f_path, mode='r') as f:
        # async for doc in ijson.items_async(f, 'posts.row.item'):
            # await yield_(doc)



async def insert(coll, documents):

    print("Inserting documents to {}...".format(coll.name))
    st = time.time()
    await coll.insert_many(documents)
    print(green("Done!"))
    print("Inserting {} took {:.5f} seconds.\n".format(coll.name, time.time() - st))


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


def getDirPath(*args) -> str:
    '''
    Reads json files and returns the list of MongoDB documents corresponding to each file.
    '''
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

    return dir_path
            
    # return [serializeDocumentsFrom(dir_path, f_name) for f_name in args]


# def serializeDocumentsFrom(dir_path, f_name):
	
    # collName = f_name[:-5].lower()
    # print("Loading {}...".format(f_name))
    # with open(os.path.join(dir_path, f_name), 'r') as f:
        # return json.load(f)[collName]['row']
    
	
def jsonFilesExistIn(dir_path, filenames):
        
    return all((os.path.isfile(os.path.join(dir_path, f_name)) for f_name in filenames))





