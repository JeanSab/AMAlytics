import praw
import math

class User(Object):

    def __init__(self, userId, r, loadProfile=False):

        self.user = r.redditor(userId)
        self.name = userId
        self.info = self.userInfo()
        if loadProfile:
            self.comments = self.getSubmitedComments()
            self.posts = self.getSubmitedPosts()

    @property
    def comments(self):
        if not hasattr(self, "comments"):
            self.comments = self.getSubmitedComments

    @property
    def posts(self):
        if not hasattr(self, 'posts'):
            self.posts = self.getSubmitedPosts

    def getSubmitedPosts(self, limit=100, listingType="new", verbose=True):
        """
        get user submission information
        """
        if verbose is True:
            print("getting info for " + str(author.name))
        subNames = {}
        for s in getattr(self.user.submissions, listingType)(limit=limit):
            if str(s.subreddit) in subNames:
                subNames[str(s.subreddit)] += 1
            else:
                subNames[str(s.subreddit)] = 1

        return subNames


    def getSubmitedComments(self, limit=100, listingType="new", verbose=True):
        """
        get user comment information
        """
        if verbose is True:
            print("getting info for " + str(author.name))
        subPosts = {}
        for s in getattr(self.user.comments, listingType)(limit=limit):
            if str(s.subreddit) in subPosts:
                subPosts[str(s.subreddit)] += 1
            else:
                subPosts[str(s.subreddit)] = 1

        return subPosts


    def userInfo(self):
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
        return {"creation_date" : self.user.created_utc, "comment_karma": self.user.comment_karma, "link_karma": self.user.link_karma}

    def compare(self, userB):

        compDict = {}
        compDict["info"] = {"1": self.name, "2": userB.name}
        compDict["creation_date"] = math.abs(self.info["creation_date"] - userB.info["creation_date"])
        compDict["comment_karma"] = math.abs(self.info["comment_karma"] - userB.info["comment_karma"])
        compDict["link_karma"] = math.abs(self.info["link_karma"] - userB.info["link_karma"])

        return compDict





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


def compare(userA, userB):
    pass

def _sigmoid(x):
    return 1 / (1 + math.exp(-x))
