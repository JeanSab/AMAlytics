import praw




def getSubmitedSubs(author, limit=100, listingType="new"):
    """
    get user submission information
    """
    subNames = {}
    for s in getattr(author.submissions, listingType)(limit=limit):
        if str(s.subreddit) in subNames:
            subNames[str(s.subreddit)] += 1
        else:
            subNames[str(s.subreddit)] = 1
        
    return subNames
    
    
def getSubmitedComments(author, limit=100, listingType="new"):
    """
    get user comment information
    """
    subPosts = {}
    
    for s in getattr(author.comments, listingType)(limit=limit):
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
    
        
    


