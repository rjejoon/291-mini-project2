import json
import time
import os
import traceback

from pymongo import MongoClient
from pymongo.collation import Collation

from phase1.extractTermsFrom import extractTermsFrom
from bcolor.bcolor import green, warning


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

        # TODO reduce insertion time. current : 120 sec
        print("\nSearching and loading three json files...")
        st = time.time()
        postDocs, tagDocs, voteDocs = loadAllDocumentsFrom('Posts.json', 'Tags.json', 'Votes.json')
        print(green("Done!"))
        print("Loading took {:.5f} seconds.\n".format(time.time() - st))

        print("Extracting terms from posts documents...")
        st = time.time()
        for postDoc in postDocs:
            postDoc['terms'] = extractTermsFrom(postDoc)
        print(green("Done!"))
        print("Extracting terms took {:.5f} seconds.\n".format(time.time() - st))

        print("Inserting documents to collections...")
        st = time.time()
        posts.insert_many(postDocs, ordered=False)
        votes.insert_many(voteDocs, ordered=False)
        tags.insert_many(tagDocs, ordered=False)
        print(green("Done!"))
        print("Insertion took {:.5f} seconds.\n".format(time.time() - st))

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
        print(e)
        return 1

    except:
        print(traceback.print_exc())
        return 2

    finally:
        print("Disconnecting from MongoDB...")
        client.close()


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


def loadAllDocumentsFrom(*args) -> list:
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

    if dir_path is None:
        raise Exception("could not find json files")
            
    return [serializeDocumentsFrom(dir_path, f_name) for f_name in args]


def serializeDocumentsFrom(dir_path, f_name):
	
    collName = f_name[:-5].lower()
    print("Loading {}...".format(f_name))
    with open(os.path.join(dir_path, f_name), 'r') as f:
        return json.load(f)[collName]['row']
    
	
def jsonFilesExistIn(dir_path, filenames):
	
    return all((os.path.isfile(os.path.join(dir_path, f_name)) for f_name in filenames))





