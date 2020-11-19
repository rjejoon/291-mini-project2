from datetime import date

from pymongo import MongoClient

from phase1.extractTermsFrom import extractTermsFrom
from phase2.getValidInput import getValidInput
from bcolor.bcolor import warning
from bcolor.bcolor import green


def postQ(db, uid) -> bool:
    posts = db['posts']
    pid = genPID(posts)

    posted = None
    while posted is None:
        
        title = input("\nEnter your title: ")
        body = input("Enter your body text: ")
        tags = getTags()
        crdate = str(date.today())  # TODO use date function built in mongo

        if confirmInfo(title, body, tags):

            post = {
                    "Id": pid,
                    "PostTypeId": "1",
                    "CreationDate": crdate,
                    "Score": 0,
                    "ViewCount": 0,
                    "Body": body,
                    "OwnerUserId": uid,
                    "Title": title,
                    "AnswerCount": 0,
                    "CommentCount": 0,
                    "FavoriteCount": 0,
                    "ContentLicense": "CC BY-SA 2.5"
                }

            # delete OwnerUserId field if user is anonymous
            if uid == '':
                del post['OwnerUserId'] 
            
            # TODO update index
            terms = extractTermsFrom(post)
            if len(terms) > 0:
                post["terms"] = terms

            if tags:
                post["Tags"] = tags
                
            posts.insert_one(post)

            print()
            print(green("Question Posted!"))

            posted = True
        
        if posted is None:
            prompt = "Do you still want to post a question? [y/n] "
            if getValidInput(prompt, ['y', 'n']) == 'n':
                posted = False

    return posted


def postAns(db, uid, parentPid) -> bool:
    posts = db['posts']
    pid = genPID(posts)

    posted = None
    while posted is None:
        
        body = input("\nEnter your body text: ")
        prompt = 'Do you want to post this answer to the selected post? [y/n] '
        
        if getValidInput(prompt, ['y','n']) == 'y':

            crdate = str(date.today())  # TODO use mongo date function
            post = {
                        "Id": pid,
                        "PostTypeId": "2",
                        "ParentId": parentPid,
                        "CreationDate": crdate,
                        "Body": body,
                        "OwnerUserId": uid,
                        "Score": 0,
                        "CommentCount": 0,
                        "ContentLicense": "CC BY-SA 2.5"
                    }

            # delete OwnerUserId field if user is anonymous
            if uid == '':
                del post['OwnerUserId'] 

            # TODO update index
            terms = extractTermsFrom(post)
            if len(terms) > 0:
                post["terms"] = terms
                
            posts.insert_one(post)

            print()
            print(pid)
            print(green("Answer Posted!"))

            posted = True

        if posted is None:
            prompt = "Do you still want to post an answer? [y/n] "
            if getValidInput(prompt, ['y', 'n']) == 'n':
                posted = False
        
    return posted

def genPID(posts) -> str:

    cursor = posts.aggregate([
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

