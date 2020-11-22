from pymongo import MongoClient
from collections import OrderedDict
from phase2.getValidInput import getValidInput
from bcolor.bcolor import pink, errmsg, cyan, bold
import os
import pprint
import time


def searchQ(db):
    '''
    Searches for question posts using the keywords the user has entered
    Prompts the user to perform various action after selecting a post

    Input:
        db -- pymongo.database.Database
    Return:
        targetPost -- list
        action -- str
    '''
    os.system('clear')
    print(pink('< Search for Questions >'))

    posts = db["posts"]
    kwList = getKeywords()
    resultList = findMatch(posts, kwList)

    targetPost = action = None
    if len(resultList) > 0:
        no, action = displaySearchResult(resultList, posts)
        targetPost = resultList[no]
    else:
        print(errmsg('error: there is no matching post.'))
    
    return targetPost, action


def getKeywords():
    '''
    Prompts the user to enter some keywords to search for question posts
    Returns a list of keywords
    '''
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
            print(errmsg("error: keywords cannot be empty."))

    return kwList


def findMatch(posts, kwList):
    '''
    Searches for the matching post using kwList and returns resultList

    Inputs:
        posts -- pymongo.collection.Collection
        kwList -- list
    Return:
        resultList -- list
    '''
    cursor = posts.find(
             {"$and": [{"terms": {"$in": kwList}},
                                {"PostTypeId":"1"}]}
             ).collation({"locale": "en", "strength":2})    # collation strength :2 --> case-insensitive

    st = time.time()
    resultList = list(cursor)
    # TODO matches
    for kw in kwList:
        for doc in resultList:
            doc['match'] = doc['terms'].count(kw)

    resultList.sort(key=lambda doc:doc['match'], reverse=True)
    print(len(resultList))

    # TODO when a keyword is < 3, search title and body instead of terms

    print("Searching took {:5} seconds.".format(time.time() - st))

    return resultList


def displaySearchResult(resultList, posts):
    '''
    Displays the matching posts from the highest number of matches to the lowest
    Displays 5 posts at once and prompts the user to view more posts and to select a post
    After selecting a post, prompts the user to choose which action to perform next

    * REMARK: This function was made by referring to action.displaySearchResult() function from mini-project1 *

    Inputs:
        resultList -- list
        posts -- pymongo.collection.Collection

    Return:
        no -- int
        action -- str
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

        opt = getValidInput(prompt, validEntries) 

        # post is selected
        if opt.isdigit():
            no = int(opt) - 1      # to match zero-index array
            displaySelectedPost(resultList, posts, no)
            action = getAction()
            choseAction = True

    return no, action


def printSearchResult(resultList, currRowIndex, limit=5):
    '''
    Displays the search result
    
    Inputs:
        resultList -- list
        currRowIndex -- int
        limit -- int (5)
    Return:
        currRowIndex -- int
    '''
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
    '''
    Displays all of the fields of the selected post

    Inputs:
        resultList -- list
        posts -- pymongo.collection.Collection
        no -- int
    '''
    # increment the view count by 1
    posts.update({"Id": resultList[no]["Id"]}, 
                {"$inc": {"ViewCount": 1}})

    targetDoc = posts.find_one({"Id": resultList[no]["Id"]})

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

    print(cyan('\nSelected Post Information:'))
    for field in fieldNames:
        if field in targetDoc:
            print('{0}: {1}'.format(bold(field), targetDoc[field]))
    print()

    
def getAction():
    '''
    Displays the available actions and trompts the user to choose the next action.
    Return:
        action -- str
    '''
    actionDict = availableActions()

    print("Choose an option to:\n")
    for cmd, action in actionDict.items():
        print("   {0}: {1}".format(bold(cmd), action))

    action = getValidInput('\nEnter a command: ', actionDict.keys())
    return action 


def availableActions():
    '''
    Creates a dictionary of the available actions
    Return:
        actionDict -- dict
    '''
    actionDict = OrderedDict()

    quesActionDict = OrderedDict()
    actionDict['pa'] = 'Post an Answer' 
    actionDict['la'] = 'List Answers'
    actionDict['vp'] = 'Vote on a post'
    actionDict['bm'] = 'Back to Menu'

    return actionDict

