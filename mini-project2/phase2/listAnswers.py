from pymongo import MongoClient

#from bcolor.bcolor import bold 


def listAnswers(posts, targetQ: dict):

    # "aa": accepted answer
    aaDoc = None
    aaId = None
    if 'AcceptedAnswerId' in targetQ:
        aaId = targetQ['AcceptedAnswerId']
        aaDoc = posts.find({ "Id": { "$eq": aaId }}).next()
    
    aDocs = posts.find({"$and": [{ "PostTypeId": "2" },
                                 { "Id": { "$ne": aaId } },
                                 { "ParentId": { "$eq": targetQ["Id"] }}]})

    ansDocs = []

    i = 0
    if aaDoc:
        ansDocs.append(aaDoc)
        printAnswerDocumentSimple(aaDoc, i, True)
        i += 1
    
    for doc in aDocs:
        ansDocs.append(doc)
        printAnswerDocumentSimple(doc, i)
        i += 1
    
    # no answer for the selected question
    if i == 0:
        return False

    interval = "[1]" if i == 0 else "[1-{}]".format(i) 
    prompt = "Select an answer {} ".format(interval)
    no = getValidInput(prompt, list(map(str, range(1, i+1))))
    no = int(no) - 1    # to match zero-index

    selectedAnsDoc = ansDocs[no]

    # TODO promptAnswerAction()
    action = promptAnswerAction()


def printAnswerDocumentSimple(doc, i, isAA=False):

    lim = 80
    crDate = doc['CreationDate']
    crDate = "{} {} UTC".format(crDate[:10], crDate[11:])
    body = doc['Body'][:lim]
    score = doc['Score']
    header = "Answer {}".format(i+1).center(80, '-')
    if isAA:
        header += ' ' + "\N{WHITE MEDIUM STAR}"

    print(header)
    print()
    print(body)
    print()
    print("{}: {}".format(bold("Creation Date"), crDate))
    print("{}: {}".format(bold("Score"), score))
    print()


def getValidInput(prompt: str, validEntries: list) -> str:

    while True:
        entry = input(prompt)
        if entry in validEntries:
            return entry
        print(errmsg("error: invalid entry"))




# TODO get rid of this function and import from the module
def bold(s):
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    return BOLD + s + ENDC


    


if __name__ == '__main__':

    client = MongoClient()
    db = client['291db']

    posts = db['posts']

    postdoc = posts.find_one()
    listAnswers(posts, postdoc)

    


