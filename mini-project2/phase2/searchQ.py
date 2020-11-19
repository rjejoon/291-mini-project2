from pymongo import MongoClient
from collections import OrderedDict
from bcolor import bcolor
import os


def searchQ(db):
    os.system('clear')
    print(bcolor.pink('< Search for Questions >'))

    posts = db["posts"]
    kwStr = getKeywords()
    resultList = findMatch(posts,kwStr)

    targetPost = action = None
    if len(resultList) > 0:
        no, action = displaySearchResult(resultList, posts)
        targetPost = resultList[no]
    else:
        print(bcolor.errmsg('error: there is no matching post.'))
    
    return targetPost, action


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
            print(bcolor.errmsg("error: keywords cannot be empty."))

    return kwList


def findMatch(posts, kwList):


    cursor = posts.aggregate([
            {"$match": {"PostTypeId":"1"}},
            {"$project": {
                            "Id": 1,
                            "AcceptedAnswerId": 1,
                            "Title": 1,
                            "CreationDate": 1,
                            "Score": 1,
                            "AnswerCount": 1,
                            "terms": {"$cond": {
                                        "if": {"$not": "$Tags"}, "then": "$terms",
                                        "else": {  
                                                "$concatArrays": 
                                                        [
                                                            "$terms",
                                                            {"$split": [{"$substr": [{"$toLower": "$Tags"}, 1, {"$subtract": [{"$strLenCP": "$Tags"}, 2]}]},"><"]}

                                                        ]
                                                }}
                                    }
                        }
            },
            {"$match": {"terms": {"$in": kwList}}},
            {"$unwind": "$terms"},
            {"$match": {"terms": {"$in": kwList}}},
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
        match = currRow['match']
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
        #TODO delete
        row += '{:^5}'.format(match)
        print(row)
        print('-'*len(colName))

        currRowIndex += 1

    return currRowIndex


def displaySelectedPost(resultList, posts, no):

    # increment the view count by 1
    posts.update({"Id": resultList[no]["_id"]}, 
                {"$inc": {"ViewCount": 1}})

    targetDoc = posts.find_one({"Id":resultList[no]["_id"]})

    fieldNames = [
                    'Id',
                    'PostTypeId', 
                    'AcceptedAnswerId',
                    'Title', 
                    'Body', 
                    'Tags', 
                    'CreationDate', 
                    'OwnerUserId', 
                    'Score',
                    'ViewCount', 
                    'AnswerCount', 
                    'CommentCount', 
                    'FavoriteCount', 
                    'LastEditorUserId', 
                    'LastEditDate', 
                    'Last Activity Date', 
                    'ContentLicense'
                ]

    print(bcolor.cyan('\nSelected Post Information:'))
    for field in fieldNames:
        if field in targetDoc:
            print('{0}: {1}'.format(bcolor.bold(field), targetDoc[field]))
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
    actionDict['pa'] = 'Post an Answer' 
    actionDict['la'] = 'List Answers'
    actionDict['vp'] = 'Vote on a post'
    actionDict['bm'] = 'Back to Menu'

    return actionDict


def validInput(prompt, entries):
    while True:
        i = input(prompt).lower()
        if i in entries:
            return i 
        print(bcolor.errmsg("error: invalid entry\n"))

