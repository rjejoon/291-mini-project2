from pymongo import MongoClient
from datetime import datetime
from bcolor import bcolor
from phase1.extractTermsFrom import extractTermsFrom
from phase2.getValidInput import getValidInput


def postQ(db, uid):

    print(bcolor.pink('\n< Post a Question >'))

    postsColl = db['posts']
    tagsColl = db['tags']
    pid = genID(postsColl)

    valid = False
    while not valid:
        
        title = input("Enter your title: ")
        body = input("Enter your body text: ")
        tagList, tagStr = getTags()
        crdate = str(datetime.now()).replace(' ', 'T')[:-3]

        validEntry = confirmInfo(title, body, tagStr)

        if validEntry:

            post = createQDict(pid, crdate, body, title)
            
            if uid:
                post["OwnerUserId"] = uid

            terms = extractTermsFrom(post)
            if len(terms) > 0:
                post["terms"] = terms

            if len(tagList) > 0:
                post["Tags"] = tagStr
                insertTags(tagsColl, tagList)
                
            postsColl.insert_one(post)
            valid = True

            print(bcolor.green("\nQuestion Posted!"))
        
        else:
            prompt = "Do you still want to post a question? [y/n] "
            uin = validInput(prompt,['y','n'])
            if uin == 'n':
                valid = True
    print()


def postAns(posts, uid, targetPid):

    print(bcolor.pink('\n< Post an Answer >'))

    pid = genID(posts)

    valid = False
    while not valid:
        
        body = input("Enter your body text: ")
        crdate = str(datetime.now()).replace(' ', 'T')[:-3]

        prompt = 'Do you want to post this answer to the selected post? [y/n] '
        uin = validInput(prompt, ['y','n'])

        if uin == 'y':

            post = createAnsDict(pid, targetPid, crdate, body, uid)

            if uid:
                post["OwnerUserId"] = uid

            terms = extractTermsFrom(post)
            if len(terms) > 0:
                post["terms"] = terms
                
            posts.insert_one(post)
            valid = True

            print(bcolor.green("\nAnswer Posted!"))

        else:
            prompt = "Do you still want to post an answer? [y/n] "
            uin = validInput(prompt,['y','n'])
            if uin == 'n':
                valid = True
    print()
        

def genID(posts) -> str:

    cursor = posts.aggregate([
        {"$group": {"_id": None, "maxId": {"$max": {"$toInt": "$Id"}}}}
    ])
    maxId = 0
    for doc in cursor:
        maxId = doc['maxId']
    
    return str(int(maxId)+1)


def getTags():
    '''
    Prompts the user for the tags and returns tagList and tagStr
    '''
    tags = input("Enter zero or more tags, each separated by a comma: ")

    tagList = []
    for tag in tags.split(','):
        tag = tag.strip()
        if tag and not tag in tagList:
            tagList.append(tag)

    tagStr = ''
    if len(tagList) > 0:
        tagStr = '<'+'><'.join(tagList)+'>'
    
    return tagList, tagStr


def createQDict(pid, crdate, body, title):

    post = {
                "Id": pid,
                "PostTypeId": "1",
                "CreationDate": crdate,
                "Score": 0,
                "ViewCount": 0,
                "Body": body,
                "Title": title,
                "AnswerCount": 0,
                "CommentCount": 0,
                "FavoriteCount": 0,
                "ContentLicense": "CC BY-SA 2.5"
            }

    return post


def createAnsDict(pid, targetPid, crdate, body, uid):

    post = {
                "Id": pid,
                "PostTypeId": "2",
                "ParentId": targetPid,
                "CreationDate": crdate,
                "Body": body,
                "Score": 0,
                "CommentCount": 0,
                "ContentLicense": "CC BY-SA 2.5"
            }
    
    return post


def insertTags(tagsColl, tags):
    '''
    Checks if the tags the user has entered already exists in tags collection
    Increments its count by one if exists; otherwise inserts a new doc with the tagName provided in the collection
    '''
    for tagName in tags:
        cursor = tagsColl.find_one({"TagName": tagName})
        if cursor:
            tagsColl.update({"TagName": tagName},{"$inc": {"Count": 1}})
        else:
            tagId = genID(tagsColl)
            tag = {
                "Id": tagId,
                "TagName": tagName,
                "Count": 1
            }
            tagsColl.insert_one(tag)


def confirmInfo(title, body, tags):
    if not tags:
        tags = 'N/A'

    print(bcolor.bold("\nPlease double check your information:"))
    print("     Title: {}".format(title))
    print("     Body: {}".format(body))
    print("     Tags: {}".format(tags))
    print()

    prompt = "Is this correct? [y/n] "
    uin = getValidInput(prompt, ['y','n'])

    return True if uin == 'y' else False
