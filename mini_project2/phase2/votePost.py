from datetime import datetime

from bcolor.bcolor import green, warning, pink, errmsg
from phase2.getValidInput import getValidInput
from phase2.postQA import genID

def votePost(votes, uid, targetPid) -> bool:
    '''
    Prompts the user to vote on the selected post
    The user is allowed to vote on the same post only once
    Inserts the vote info into votes collection with a unique vid

    Inputs:
            votes -- pymongo.collection.Collection
            uid -- str
            targetPid 
    '''
    # TODO optimize running time
    # TODO score not updated
    print(pink('\n< Vote Post >'))
    
    prompt = warning('Confirmation: Do you want to vote on this post? [y/n] ')
    uin = getValidInput(prompt, ['y', 'n'])

    cursor = votes.find_one({"$and": [{"UserId": uid}, 
                                      {"PostId": targetPid}]})
    
    if cursor:
        print(errmsg("error: you've already voted on this post."))
        return False
        
    if uin == 'y':
        vid = genID(votes)
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
        print(green('\nVoting Completed!'))

    print()
    return True
