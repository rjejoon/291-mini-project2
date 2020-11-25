from datetime import datetime

from bcolor.bcolor import green, warning, pink, errmsg
from phase2.getValidInput import getValidInput


def votePost(db, maxIdDict, uid, targetPid) -> bool:
    '''
    Prompts the user to vote on the selected post
    The user is allowed to vote on the same post only once
    Inserts the vote info into votes collection with a unique vid

    Inputs:
        db -- pymongo.database.Database
        maxIdDict -- dict
        uid -- str
        targetPid 
    Return:
        bool
    '''
    posts = db['posts']
    votes = db['votes']

    print(pink('\n< Vote Post >'))
    
    prompt = warning('Confirmation: Do you want to vote on this post? [y/n] ')
    uin = getValidInput(prompt, ['y', 'n'])

    if uin == 'n':
        return False

    cursor = None
    if uid != '':
        cursor = votes.find_one({"$and": [{"UserId": uid}, 
                                          {"PostId": targetPid}]})

    if cursor:
        print(errmsg("error: you've already voted on this post."))
        return False
        
    vid = str(maxIdDict['votes'] + 1)
    maxIdDict['votes'] += 1

    crdate = str(datetime.now()).replace(' ', 'T')[:-3]
    vote = {
            "Id"          : vid,
            "PostId"      : targetPid,
            "VoteTypeId"  : 2,
            "CreationDate": crdate
    }
    
    if uid:
        vote['UserId'] = uid
    
    votes.insert_one(vote)
    posts.update(
            {"Id": targetPid},
            { "$inc": { "Score": 1 } } 
            )
    
    print(green('\nVoting Completed!'))

    print()
    return True
