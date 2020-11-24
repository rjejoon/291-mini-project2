import os
import json

from phase1.extractTermsFrom import extractTermsFrom

from bcolor.bcolor import green


cpdef list serializeDocumentsFrom(str dir_path, str f_name):
    '''
    Loads and serializes a json file. Extract terms from title, body, and tags if the data is for posts.
    Returns the data in a list.
    '''
    cdef list docs
    collName = f_name[:-5].lower()
    print("Loading {}...".format(f_name))
    with open(os.path.join(dir_path, f_name), 'r') as f:
        docs = json.load(f)[collName]['row']
        if collName == 'posts':
            print("Extracting terms from posts...")
            for doc in docs:
                doc['terms'] = extractTermsFrom(doc)
            print(green("Done!"))

    return docs
