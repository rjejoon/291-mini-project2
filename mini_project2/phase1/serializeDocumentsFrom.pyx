import os
import json

from phase1.extractTermsFrom import extractTermsFrom


cpdef list serializeDocumentsFrom(str dir_path, str f_name):

    cdef list docs
    collName = f_name[:-5].lower()
    print("Loading {}...".format(f_name))
    with open(os.path.join(dir_path, f_name), 'r') as f:
        docs = json.load(f)[collName]['row']
        if collName == 'posts':
            for doc in docs:
                doc['terms'] = extractTermsFrom(doc)

    return docs


