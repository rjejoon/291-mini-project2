from pymongo import MongoClient
from datetime import date
from phase1.extractTermsFrom import extractTermsFrom
from phase1.filterTerms import filterTerms


def postQ(db, uid):

    posts = db['posts']
    tags = db['tags']
    votes = db['votes']

    valid = False
    while not valid:
        pid = getPID(posts)
        print('done')
        title = input("Enter your title: ")
        body = input("Enter your body text: ")
        tags = getTags()
        crdate = str(date.today())

        validEntry = confirm(title, body, tags)

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
            if tags:
                post["Tags"] = tags

            terms = filterTerms(extractTermsFrom(post))
        
            posts.insert_one(post)
            valid = True


def getPID(posts):
    #pipeline = [
    #{"$group":{ "_id":"null","maxId":{"$max":"$Id"}}}
    #]
    #maxid = posts.aggregate(pipeline)
    #print(type(maxid))
    #print(list(maxid))
    
    cursor = posts.aggregate([
        {"$group": {"_id": None, "maxId": {"$max": {"$toInt": "$Id"}}}}
        ])
    maxId = cursor.next()['maxId']

    pid = str(maxid+1)
    return pid

def getTags():
    tags = input("Enter zero or more tags, each separated by a comma: ")
    taglst = []
    for tag in tags.split(','):
        tag = tag.strip()
        if tag:
            taglst.append(tag)
    if len(taglst) > 0:
        tagStr = ''
        for tag in taglst():
            tagStr += '<'+tag+'>'
        return tagStr
    else:
        return None

    



def confirm(title, body, tags):
    print("Please double check your information")
    print("     Title: {}".format(title))
    print("     Body: {}".format(body))
    print("     Tags: {}".format(tags))
    print()

    prompt = "Is this correct? [y/n]"
    uin = validInput(prompt, ['y','n'])
    return True if uin == 'y' else False

def validInput(prompt, entries):
    while True:
        i = input(prompt).lower()
        if i in entries:
            return i 
        print("error: invalid entry\n")

main()
