import time
import re
from collections import OrderedDict

from pymongo import MongoClient

from phase2.clear import clear
from phase2.getValidInput import getValidInput
from bcolor.bcolor import pink, errmsg, cyan, bold, warning


def searchQ(db):
    '''
    Prompts the user for one or more keywords, and 
    searches for any question posts that have terms equal to the given keywords.
    Prompts the user to perform various actions after selecting a post.

    Input:
        db -- pymongo.database.Database
    Return:
        targetPost -- list
        action -- str
    '''
    clear()
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


def getKeywords() -> list:
    '''
    Prompts the user to enter some keywords to search for question posts
    Returns a list of keywords
    '''
    prompt = "Enter keywords to search, each separated by a comma: "
    valid = False 
    while not valid:
        keywords = input(prompt).strip().lower().split(',')
        kwSet = {kw.strip() for kw in keywords if len(kw) > 0}
        if len(kwSet) > 0:
            valid = True
        else:
            print(errmsg("error: keywords cannot be empty."))

    return list(kwSet) 


def findMatch(posts, kwList) -> list:
    '''
    Finds all posts with any matching words in kwList and returns them.

    Inputs:
        posts -- pymongo.collection.Collection
        kwList -- list
    Return:
        resultList -- list
    '''
    st = time.time()
<<<<<<< HEAD
    kwList1 = []
    kwList2 = []
    resultList = []
    for kw in kwList:
        if len(kw) >= 3:
            kwList1.append(kw)
        else:
            kwList2.append(kw)

    cursor1 = list(posts.find(
=======
    cursor = posts.find(
>>>>>>> eb22e0ed0a91c49b61e47b7670c92332fa365744
             {"$and": [{"terms": {"$in": kwList1}},
                                {"PostTypeId":"1"}]}
             ).collation({"locale": "en", "strength": 2}))   # collation strength :2 --> case-insensitive

    [resultList.append(each) for each in cursor1]

<<<<<<< HEAD
    if len(kwList2) > 0:
        # TODO partial search if we have time 
        # cursor2 = posts.find({ "terms": { "$regex": /789$/ } })
        # cursor2 = posts.aggregate([
        #     {"$match":
        #         {
        #             "$expr":
        #
        #                 {"$gt":
        #                     [
        #                         {"$function":
        #                             {
        #                                 "body": '''
        #                                         function(title, body, tags, kwList) {
        #
        #                                             const match = kwList.reduce((accum, kw) => {
        #                                                 accum + (title.length - title.replace(kw, '').length) / kw.length +
        #                                                 (body.length - body.replace(kw, '').length) / kw.length +
        #                                                 (tags.length - tags.replace(kw, '').length) / kw.length;
        #                                             });
        #                                             return (match > 0 ? true : false );
        #                                         }
        #                                         ''',
        #                                 "args": [ "$Title", "$Body", "$Tags", kwList2 ],
        #                                 "lang": 'js'
        #                             }
        #                         },0
        #                     ]
        #
        #                 }
        #         }
        #     }
        # ])

        for kw in kwList2:
            cursor2 = list(posts.find(
                {"$and": [
                    {"$or": [
                        {"Title": {"$regex": '.*{}.*'.format(kw), '$options': 'i'}},
                        {"Body": {"$regex": '.*{}.*'.format(kw), '$options': 'i'}},
                        {"Tags": {"$regex": kw, '$options': 'i'}}
                    ]},
                    {'PostTypeId': '1'}
                ]}
            ).collation({"locale": "en", "strength": 2}))
            [resultList.append(each) for each in cursor2]
    
=======
>>>>>>> eb22e0ed0a91c49b61e47b7670c92332fa365744
    print("Searching took {:5} seconds.".format(time.time() - st))

    return list(cursor) 


def displaySearchResult(resultList, posts):
    '''
    Displays the matching posts 
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
                    '_id',
                    'Id',
                    'PostTypeId', 
                    'AcceptedAnswerId',
                    'Title', 
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
                    'LastActivityDate', 
                    'ContentLicense',
                    'terms',
                    'Body'
                ]

    # ensure all the fields are included
    for f in targetDoc:
        if f not in fieldNames:
            fieldNames.append(f)

    clear()
    print(cyan('Selected Post Information:\n'))
    for f in fieldNames:
        if f in targetDoc:
            fieldElem = targetDoc[f]
            if f in ('CreationDate', 'LastActivityDate'):
                fieldElem = "{} {} UTC".format(fieldElem[:10], fieldElem[11:])
            elif f == 'Body':
                fieldElem = '\n\n' + fieldElem
            print("{}: {}".format(bold(f), fieldElem))
    
def getAction():
    '''
    Displays the available actions and trompts the user to choose the next action.
    Return:
        action -- str
    '''
    actionDict = availableActions()

    print("\nChoose an option to:\n")
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

