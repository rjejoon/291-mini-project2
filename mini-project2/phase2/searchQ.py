from pymongo import MongoClient
from collections import OrderedDict

from bcolor.bcolor import errmsg


def searchQ(db):

    posts = db["posts"]
    kwList = getKeywords()
    resultList = findMatch(posts, kwList)

    if len(resultList) > 0:
        no, action = displaySearchResult(resultList, posts)
        return resultList[no], action
    else:
        # TODO must return 2 things
        print(errmsg('error: there is no matching post.'))


def getKeywords():

    prompt = "Enter keywords to search, each separated by a comma: "
    valid = False 
    while not valid:
        keywords = input(prompt).lower().split(',')
        kwList = []
        for keyword in keywords:
            keyword = keyword.strip()
            if keyword and keyword not in kwList:
                kwList.append(keyword)
        
        if len(kwList) > 0:
            valid = True
        else:
            print("error: keywords cannot be empty.")

    return kwList


def findMatch(posts, kwList):

    # TODO bug: # of matches are too large

    cursor = posts.aggregate([
        {"$match": {"PostTypeId":"1"}},
        {"$project": {
                        "Id": 1,
                        "Title": 1,
                        "CreationDate": 1,
                        "Score": 1,
                        "AnswerCount": 1,
                        "terms": 1,
                        "tagarr": {         # split tags into an array
                                    "$split": [{"$substr": [
                                                        "$Tags", 
                                                        1, 
                                                        {"$subtract": [{"$strLenCP": "$Tags"}, 2]}
                                                    ]
                                                }, 
                                                "><"]
                                    }
                        }
        },

        {"$match": { "$or": [ {"terms": {"$in": kwList}}, {"tagarr": {"$in": kwList}} ] }},
        {"$unwind": "$terms"},
        {"$unwind": "$tagarr"},
        {"$match": { "$or": [ {"terms": {"$in": kwList}}, {"tagarr": {"$in": kwList}} ] }},
        {"$group": {"_id": "$Id", 
                    "Title": {"$first": "$Title"},
                    "CreationDate": {"$first": "$CreationDate"}, 
                    "Score": {"$first": "$Score"}, 
                    "AnswerCount": {"$first": "$AnswerCount"},
                    "match": {"$sum": 1}}},
        {"$sort": {"match": -1}}
    ])
    
    return list(cursor)


def displaySearchResult(resultList, posts):
    '''
    This function was made by referring to action.displaySearchResult() function from mini-project1
    '''
    currRowIndex = 0 
    numRows = len(resultList)
    no = action = domain = None
    validEntries = [] 
    choseAction = False

    while not choseAction and currRowIndex < numRows:
        currRowIndex = printSearchResult(resultList, currRowIndex)

        domain = '1-{}'.format(currRowIndex) if currRowIndex > 1 else '1'
        remainingRows = numRows - currRowIndex

        if remainingRows > 0:
            suffix = 's' if remainingRows > 1 else ''
            print("There are {} more row{} to display.\n".format(remainingRows, suffix))
            prompt = "Press enter to view more, or pick no. [{}] to select: ".format(domain)
            validEntries = ['y', '']
        else:
            prompt = "Search hit bottom. Pick no. [{}] to select: ".format(domain)
            validEntries = []

        if len(domain) == 1:
            # there is only one post to choose. 
            validEntries.append('1')
        else:
            end = domain.split('-')[1]
            validEntries += list(map(str, range(1, int(end)+1)))  

        opt = validInput(prompt, validEntries) 

        # post is selected
        if opt.isdigit():
            no = int(opt) - 1      # to match zero-index array
            displaySelectedPost(resultList, posts, no)
            action = getAction()
            choseAction = True

    return no, action


def printSearchResult(resultList, currRowIndex, limit=5):

    colName = ' {:^5} | {:^40} | {:^15} | {:^8} | {:^15}'.format('No.','Title','Creation Date','Score','Answer Count')
    frame = '='*len(colName)
    print(frame)
    print(colName)
    print('-'*len(colName))

    if currRowIndex+limit > len(resultList):
        limit = len(resultList)%limit
 
    for i in range(currRowIndex, currRowIndex + limit):
        currRow = resultList[i]
        title = currRow['Title']
        crdate = currRow['CreationDate']
        score = currRow['Score']
        anscnt = currRow['AnswerCount']
        row = ' '
        row += '{:^5} | '.format(str(i+1))
        if len(title) > 37:
            title = title[:37]+'...'
        row += '{:40} | '.format(title)
        row += '{:^15} | '.format(crdate[:10])
        if not score:
            score = '0'
        row += '{:^8} | '.format(score)
        row += '{:^15}'.format(anscnt)
        print(row)
        print('-'*len(colName))

        currRowIndex += 1

    return currRowIndex

def displaySelectedPost(resultList, posts, no):

    targetId = {"Id":resultList[no]["_id"]}
    cursor = posts.aggregate([{"$match": targetId}, {"$project": {"_id": 0, "Id": 1, "ViewCount": 1}}])
    newViewCount = str(int(cursor.next()['ViewCount'])+1)

    posts.update(targetId, {"$set": {"ViewCount": newViewCount}})

    target = list(posts.find({"Id":resultList[no]["_id"]}))[0]
    
    kwList = ['Id','PostTypeId', 'Title', 'Body', 'Tags', 'CreationDate', 'OwnerUserId', 'Score','ViewCount', 
        'AnswerCount', 'CommentCount', 'FavoriteCount', 'LastEditorUserId', 'LastEditDate', 'Last Activity Date', 'ContentLicense']

    print('\nSelected Post Information:')
    for kw in kwList:
        if kw in target:
            print('    • {0}: {1}'.format(kw,target[kw]))
    print()

    
def getAction():
    actionDict = availableActions()

    print("Choose an option to:\n")
    for cmd, action in actionDict.items():
        print("   {0}: {1}".format(cmd, action))

    action = validInput('\nEnter a command: ', actionDict.keys())
    return action 


def availableActions():
    actionDict = OrderedDict()

    quesActionDict = OrderedDict()
    actionDict['wa'] = 'Write an Answer' 
    actionDict['la'] = 'List Answers'
    actionDict['vt'] = 'Vote on a post'
    actionDict['bm'] = 'Back to Menu'

    return actionDict


def validInput(prompt, entries):
    while True:
        i = input(prompt).lower()
        if i in entries:
            return i 
        print("error: invalid entry\n")

