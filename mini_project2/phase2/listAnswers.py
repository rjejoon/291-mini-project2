import os
from pymongo import MongoClient

from bcolor.bcolor import bold 
from bcolor.bcolor import cyan
from bcolor.bcolor import warning 
from phase2.getValidInput import getValidInput


def listAnswers(posts, targetQ: dict) -> bool:
    '''
    Displays all the answer corresponds to the target question post.
    An accepted answer is marked with a star.
    By selecting an answer post, a user can see all the fields in the document.

    Inputs:
        posts -- pymongo.collection.Collection
        targetQ -- dict
    Return:
        bool
    '''

    # "aa": accepted answer
    aaDoc = None
    aaId = None
    if 'AcceptedAnswerId' in targetQ:
        aaId = targetQ['AcceptedAnswerId']
        aaDoc = posts.find_one({ "Id": { "$eq": aaId }})
    
    aDocs = posts.find({"$and": [{ "PostTypeId": "2" },
                                 { "Id": { "$ne": aaId } },
                                 { "ParentId": { "$eq": targetQ["_id"] }}]})

    os.system('clear')
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
        print(warning("There is no answer post to this question."))
        return False

    interval = "[1]" if i == 1 else "[1-{}]".format(i) 
    prompt = "Select an answer {} ".format(interval)
    no = getValidInput(prompt, list(map(str, range(1, i+1))))
    no = int(no) - 1    # to match zero-index

    selectedAnsDoc = ansDocs[no]

    printAnswerDocumentFull(selectedAnsDoc)

    return promptAnswerAction()


def printAnswerDocumentFull(doc):
    '''
    Displays every field in the selected answer document.

    Inputs:
        doc -- dict
        i -- int
        isAA -- bool
    '''
    os.system('clear')
    del doc['_id']
    fieldNames = list(doc.keys())
    
    print(cyan('< Post Info>\n'))
    # TODO dict is not ordered
    for f in fieldNames:
        fieldElem = doc[f]
        if f =='CreationDate':
            fieldElem = "{} {} UTC".format(fieldElem[:10], fieldElem[11:])
        elif f == 'Body':
            fieldElem = '\n\n' + fieldElem

        print("{}: {}".format(bold(f), fieldElem), end='\n')



def printAnswerDocumentSimple(doc, i, isAA=False):
    '''
    Displays a simple version of the answer document.

    Inputs:
        doc -- dict
        i -- int
        isAA -- bool
    '''

    score = doc['Score']
    crDate = doc['CreationDate']
    crDate = "{} {} UTC".format(crDate[:10], crDate[11:])

    lim = 80
    body = doc['Body'][:lim]

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


def promptAnswerAction() -> bool:
    '''
    Return True if the user wishes to perform an answer action.
    Since there is only one answer action, boolean is returned.
    '''

    i = getValidInput(warning("Would you like to vote on this answer? [y/n] "), ['y', 'n'])

    if i == 'y':
        return True
    return False


