from pymongo import MongoClient
from datetime import date

def main():
    client = MongoClient('mongodb://localhost:27017/')
    with client:
        db = client["291db"]
        posts = db['posts']
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
            
                posts.insert_one(post)
                valid = True


def getPID(posts):
    #pipeline = [
    #{"$group":{ "_id":"null","maxId":{"$max":"$Id"}}}
    #]
    #maxid = posts.aggregate(pipeline)
    #print(type(maxid))
    #print(list(maxid))
    
    maxid = posts.find_one(sort=[("Id", -1)])
    print(maxid)
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

def extractTerms(title, body):
    pass
    



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