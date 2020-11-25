import os

from pymongo import MongoClient

from bcolor.bcolor import bold, cyan, warning, errmsg
from phase2.getValidInput import getValidInput
from phase2.clear import clear


def listAnswers(posts, targetQ: dict) -> str:
    '''
    Displays all the answers that correspond to the target question post.
    An accepted answer is displayed first and marked with a star.
    By selecting an answer post, the user can see all its field, and it returns
    its post id.

    Inputs:
        posts -- Collection
        targetQ -- dict
    Return:
        str
    '''
    # "aa": accepted answer
    aaDoc = None
    aaId = None
    if 'AcceptedAnswerId' in targetQ:
        aaId = targetQ['AcceptedAnswerId']
        aaDoc = posts.find_one({ "Id": { "$eq": aaId }})
    
    aDocs = posts.find({"$and": [{ "PostTypeId": "2" },
                                 { "Id": { "$ne": aaId } },
                                 { "ParentId": targetQ["Id"] }]})

    clear()
    ansDocs = []

    i = 0
    if aaDoc:
        ansDocs.append(aaDoc)
        printAnswerDocumentSimple(aaDoc, i, isAA=True)
        i += 1
    
    for doc in aDocs:
        ansDocs.append(doc)
        printAnswerDocumentSimple(doc, i)
        i += 1
    
    # no answer for the selected question
    if i == 0:
        print(errmsg("There is no answer post to this question."))
        return ''

    interval = "[1]" if i == 1 else "[1-{}]".format(i) 
    prompt = "Select an answer {} ".format(interval)
    no = getValidInput(prompt, list(map(str, range(1, i+1))))
    no = int(no) - 1    # to match zero-index

    selectedAnsDoc = ansDocs[no]

    printAnswerDocumentFull(selectedAnsDoc)

    return selectedAnsDoc['Id']


def printAnswerDocumentFull(doc):
    '''
    Displays every field in the selected answer document.

    Inputs:
        doc -- dict
        i -- int
        isAA -- bool
    '''
    clear()
    fieldNames = [
                    '_id',
                    'Id',
                    'PostTypeId',
                    'ParentId',
                    'CreationDate',
                    'Score',
                    'OwnerUserId',
                    'LastActivityDate',
                    'CommentCount',
                    'ContentLicense',
                    'terms',
                    'Body'
                ]

    # ensure all the fields are included
    for f in doc:
        if f not in fieldNames:
            fieldNames.append(f)

    print(cyan('< Post Info>\n'))
    for f in fieldNames:
        if f in doc:
            fieldElem = doc[f]
            if f in ('CreationDate', 'LastActivityDate'):
                fieldElem = "{} {} UTC".format(fieldElem[:10], fieldElem[11:])
            elif f == 'Body':
                fieldElem = '\n\n' + fieldElem
            print("{}: {}".format(bold(f), fieldElem))


def printAnswerDocumentSimple(doc: dict, i: int, isAA=False):
    '''
    Displays a simple version of the answer document.
    Fields to be displayed:
        1. first 80 chars of body,
        2. Creation date,
        3. Score
    '''
    score = doc['Score']
    crDate = doc['CreationDate']
    crDate = "{} {} UTC".format(crDate[:10], crDate[11:])

    LENLIM = 80
    body = doc['Body'][:LENLIM]

    header = "Answer {}".format(i+1).center(80, '-')
    if isAA:
        header += ' ' + '\N{WHITE MEDIUM STAR}'

    print(header)
    print()
    print(body)
    print()
    print("{}: {}".format(bold("Creation Date"), crDate))
    print("{}: {}".format(bold("Score"), score))
    print()
