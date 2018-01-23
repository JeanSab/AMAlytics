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
            subNames[str(s.subreddit)] = 0
        
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
            subPosts[str(s.subreddit)] = 0
        
    return subPosts
    
    
    
    
    


username = 'afirsttest'
userAgent = "afirsttest/0.1 by " + username
clientId = 'aRFvr_zLw5DU9g'
clientSecret = ""

r = praw.Reddit(user_agent=userAgent, client_id=clientId, client_secret=clientSecret)




submission = r.submission("")
comment = submission.comments[0]
author = comment.author


#user =  r.redditor(comment.author)

print(getSubmitedComments(author))
