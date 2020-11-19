from pymongo import MongoClient
from datetime import date
from phase1.extractTermsFrom import extractTermsFrom
from phase2.getValidInput import getValidInput


def postQ(db, uid):
    posts = db['posts']
    pid = genPID(posts)

    valid = False
    while not valid:
        
        title = input("\nEnter your title: ")
        body = input("Enter your body text: ")
        tags = getTags()
        crdate = str(date.today())  # TODO use date function built in mongo

        validEntry = confirmInfo(title, body, tags)

        if validEntry:

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
            
            terms = extractTermsFrom(post)
            if len(terms) > 0:
                post["terms"] = terms

            if tags:
                post["Tags"] = tags
                
            posts.insert_one(post)
            valid = True

            print()
            print("Question Posted!")
        
        if not valid:
            prompt = "Do you still want to post a question? [y/n] "
            uin = validInput(prompt,['y','n'])
            if uin == 'n':
                valid = True


def postAns(db, uid, parentPid):
    posts = db['posts']
    pid = genPID(posts)

    valid = False
    while not valid:
        
        body = input("\nEnter your body text: ")
        prompt = 'Do you want to post this answer to the selected post? [y/n] '
        uin = validInput(prompt, ['y','n'])

        if uin == 'y':

            crdate = str(date.today())
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

            terms = extractTermsFrom(post)
            if len(terms) > 0:
                post["terms"] = terms
                
            posts.insert_one(post)
            valid = True

            print()
            print(pid)
            print("Answer Posted!")

        if not valid:
            prompt = "Do you still want to post an answer? [y/n] "
            uin = validInput(prompt,['y','n'])
            if uin == 'n':
                valid = True
        

def genPID(posts) -> str:

    cursor = posts.aggregate([
        {"$group": {"_id": None, "maxId": {"$max": {"$toInt": "$Id"}}}}
    ])
    maxId = 0
    for doc in cursor:
        maxId = doc['maxId']
    
    return str(int(maxId)+1)


def getTags():
    tags = input("Enter zero or more tags, each separated by a comma: ")

    tagList = []
    for tag in tags.split(','):
        tag = tag.strip()
        if tag and not tag in tagList:
            tagList.append(tag)
    
    tagStr = '<'+'><'.join(tagList)+'>'
    
    return tagStr if tagStr else None


def confirmInfo(title, body, tags):
    if not tags:
        tags = 'N/A'

    print("Please double check your information")
    print("     Title: {}".format(title))
    print("     Body: {}".format(body))
    print("     Tags: {}".format(tags))
    print()

    prompt = "Is this correct? [y/n] "
    uin = getValidInput(prompt, ['y','n'])

    return True if uin == 'y' else False

