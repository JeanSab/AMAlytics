import praw
import math
import logging

class InvalidUserData(Exception):
    pass

class User():

    def __init__(self, userId, r, loadProfile=False):

        if userId is None or userId == "":
            raise InvalidUserData

        self.user = r.redditor(userId)
        self.name = userId
        self.info = self.userInfo()
        if loadProfile:
            self.comments
            self.posts = self.getSubmitedPosts()


    @property
    def comments(self):
        # try:
        #     return self._comments
        # except AttributeError:
        #     self._comments = self.getSubmitedComments()
        #     return self._comments

        if not hasattr(self, "_comments"):
            self._comments = self.getSubmitedComments()

        return self._comments

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
        if hasattr(self, "_commentsCustLimit"):
            return self._commentsCustLimit

        if verbose is True:
            print("getting info for " + str(self.name))
        subPosts = {}
        for s in getattr(self.user.comments, listingType)(limit=limit):
            if str(s.subreddit) in subPosts:
                subPosts[str(s.subreddit)] += 1
            else:
                subPosts[str(s.subreddit)] = 1

        self._commentsCustLimit = subPosts
        return self._commentsCustLimit

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
        return {"creation_date": self.user.created_utc,
                "comment_karma": self.user.comment_karma,
                "link_karma": self.user.link_karma}

    def compare(self, userB, limit=100):
        """Compare two users.

        Parameters
        ----------
        userB : User
            An other valid User instance.
        limit : int
            Limit for comment comparison, see User.getSubmitedComments.

        Returns
        -------
        Dict
            A dictionary with information about the comparison of the two users.

        """
        if not isinstance(userB, User):
            raise TypeError

        compDict = {}
        compDict["info"] = {"1": self.name, "2": userB.name}
        compDict["creation_date"] = abs(self.info["creation_date"] - userB.info["creation_date"])
        compDict["comment_karma"] = abs(self.info["comment_karma"] - userB.info["comment_karma"])
        compDict["link_karma"] = abs(self.info["link_karma"] - userB.info["link_karma"])

        acoms = self.getSubmitedComments(limit=limit)
        bcoms = userB.getSubmitedComments(limit=limit)
        compcoms = {}

        for k, v in acoms.items():
            if k in bcoms:
                compcoms[k] = abs(v - bcoms[k])
        compDict["comments"] = compcoms

        return compDict

    def compareScore(self, userB, limit=100):
        """Compare two user objects by getting a note.

        Parameters
        ----------
        userB : User
            An other valid User instance.
        limit : int
            Limit for comment comparison, see User.getSubmitedComments.

        Returns
        -------
        int
            The score

        """
        cmptDict = self.compare(userB, limit=limit)
        return len(cmptDict["comments"])  # TODO:devide

    def __str__(self):
        return self.name

    def __repr__(self):
        return "< " + str(self) + " >"


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
