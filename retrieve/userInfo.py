import praw




def getSubmitedSubs(author, limit=100):
    """
    get user submission information
    """
    subNames = {}
    for s in author.submissions.new():
        if str(s.subreddit) in subNames:
            subNames[str(s.subreddit)] += 1
        else:
            subNames[str(s.subreddit)] = 1
        
    return subNames
    
    
def getSubmitedComments(author):
    """
    get user comment information
    """
    subPosts = {}
    for s in author.comments.new():
        if str(s.subreddit) in subPosts:
            subPosts[str(s.subreddit)] += 1
        else:
            subPosts[str(s.subreddit)] = 1
        
    return subPosts
    

def getUpvotedComments(author):
    pass


def getUpvotedSumissions(author):
    pass
    
def userInfo(author):
    
    
    info = {"creation_date" : author.created_utc}
    
    print(dir(author))    
    



username = 'CMonShowMe'
userAgent = "afirsttest/0.1 by " + username


r = praw.Reddit('afirsttest', user_agent=userAgent)




submission = r.submission("1u1pwy")
comment = submission.comments[0]
author = comment.author


#user =  r.redditor(comment.author)

userInfo(author)


print(type(r.redditor(author.name).created_utc))
