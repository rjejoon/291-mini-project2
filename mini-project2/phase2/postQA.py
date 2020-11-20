from datetime import datetime

from pymongo import MongoClient

from phase1.extractTermsFrom import extractTermsFrom
from phase2.getValidInput import getValidInput
from bcolor.bcolor import warning
from bcolor.bcolor import green


def postQ(db, uid) -> bool:

    print(bcolor.pink('\n< Post a Question >'))

    postsColl = db['posts']
    tagsColl = db['tags']
    pid = genID(postsColl)

    posted = None
    while posted is None:
        
        title = input("Enter your title: ")
        body = input("Enter your body text: ")
        tagStr = getTags()
        crdate = str(datetime.now()).replace(' ', 'T')[:-3]

        if confirmInfo(title, body, tagStr):

            post = createQDict(pid, crdate, body, title)

            # delete OwnerUserId field if user is anonymous
            if uid == '':
                del post['OwnerUserId'] 
            
            # TODO update index

            terms = extractTermsFrom(post)
            if len(terms) > 0:
                post["terms"] = terms

            if tagStr != '':
                post["Tags"] = tagStr
                insertTags(tagsColl, tagList)
                
            postsColl.insert_one(post)

            print(green("\nQuestion Posted!"))

            posted = True
        
        else:
            prompt = "Do you still want to post a question? [y/n] "
            if getValidInput(prompt, ['y', 'n']) == 'n':
                posted = False

    return posted
        

def postAns(posts, uid, targetPid) -> bool:

    print(bcolor.pink('\n< Post an Answer >'))

    pid = genID(posts)

    posted = None
    while posted is None:
        
        body = input("Enter your body text: ")
        crdate = str(datetime.now()).replace(' ', 'T')[:-3]

        prompt = 'Do you want to post this answer to the selected post? [y/n] '
        
        if getValidInput(prompt, ['y','n']) == 'y':

            post = createAnsDict(pid, targetPid, crdate, body, uid)

            # delete OwnerUserId field if user is anonymous
            if uid == '':
                del post['OwnerUserId'] 

            # TODO update index
            terms = extractTermsFrom(post)
            if len(terms) > 0:
                post["terms"] = terms
                
            posts.insert_one(post)
            print(green("\nAnswer Posted!"))
            posted = True

        else:
            prompt = "Do you still want to post an answer? [y/n] "
            if getValidInput(prompt, ['y', 'n']) == 'n':
                posted = False

        
    return posted


def genID(collName) -> str:
    '''
    Finds the larget id in the given collection and Generates a unique id
    '''
    cursor = collName.aggregate([
        {"$group": {"_id": None, "maxId": {"$max": {"$toInt": "$Id"}}}}
    ])
    maxId = 0
    for doc in cursor:
        maxId = doc['maxId']
    
    return str(int(maxId)+1)


def getTags() -> str:

    tags = input("Enter zero or more tags, each separated by a comma: ")

    tagSet = {
                tag.strip()
                for tag in tags.split(',')
                if tag != ''
             }
    
    if len(tagSet) == 0:
        return ''
    return '<' + '><'.join(tagSet) + '>'


def createQDict(pid, crdate, body, title, uid):

    return {
                "Id": pid,
                "PostTypeId": "1",
                "OwnerUserId": uid,
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


def createAnsDict(pid, targetPid, crdate, body, uid):

    return {
                "Id": pid,
                "PostTypeId": "2",
                "OwnerUserId": uid,
                "ParentId": targetPid,
                "CreationDate": crdate,
                "Body": body,
                "Score": 0,
                "CommentCount": 0,
                "ContentLicense": "CC BY-SA 2.5"
            }
    


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


def confirmInfo(title, body, tags) -> bool:

    tags = 'N/A' if not tags else tags

    print(warning("Please double check your information:"))
    print()
    print("     Title: {}".format(title))
    print("     Body: {}".format(body))
    print("     Tags: {}".format(tags))
    print()

    prompt = "Is this correct? [y/n] "
    uin = getValidInput(prompt, ['y','n'])

    return True if uin == 'y' else False
