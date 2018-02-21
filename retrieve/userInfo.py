import praw


def getSubmitedPosts(author, limit=100, listingType="new", verbose=True):
    """
    get user submission information
    """
    if verbose is True:
        print("getting info for " + str(author.name))
    subNames = {}
    for s in getattr(author.submissions, listingType)(limit=limit):
        if str(s.subreddit) in subNames:
            subNames[str(s.subreddit)] += 1
        else:
            subNames[str(s.subreddit)] = 1

    return subNames


def getSubmitedComments(author, limit=100, listingType="new", verbose=True):
    """
    get user comment information
    """
    if verbose is True:
        print("getting info for " + str(author.name))
    subPosts = {}
    for s in getattr(author.comments, listingType)(limit=limit):
        if str(s.subreddit) in subPosts:
            subPosts[str(s.subreddit)] += 1
        else:
            subPosts[str(s.subreddit)] = 1

    return subPosts



def userInfo(author):
    """returns information from a specific author.

    Parameters
    ----------
    author : praw.models.Redditor
        a working Redditor instance.

    Returns a dictionary containing relevant information.
    -------
    type
        dict.

    """
    return {"creation_date" : author.created_utc, "comment_karma": author.comment_karma, "link_karma": author.link_karma}
