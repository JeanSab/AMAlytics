import praw


class Post(object):

    def __init__(self, postId, r, allComments=True):
        """initialize Post instance
        Parameters
        ----------
        postId : String
            reddit post id.
        r : praw.Reddit
            a working reddit instance.
        allComments : Boolean
            if True, fecthes all the comments of the post a forest.
        """

        self.r = r
        self.submission = r.submission(postId)
        self.commentTree = []
        self.id = postId
        if allComments:
            self.commentTree = self.getAllComments()

    def getAllComments(self, verbose=True):
        """Gets All comments of a submission as a tree.
        Parameters
        ----------
        verbose : Boolean
            If verbose is true, indicates when comments are being fetched via the Praw API
        Returns
        -------
        type
            a list of dictionaries representing top comments and their children.
        """
        comments = self.submission.comments #all top comments (as comment forest)
        tree = {"replies":[]}
        counter = _count()
        for comment in comments: #for all top comments, get subcomments
            self.getSubCommentsTree(comment, tree, verbose=verbose, counter=counter)
        return tree["replies"]


    def getSubCommentsTree(self, comment, parentNode, verbose=True, counter=None):
        totalFetched = str(counter())
        if not hasattr(comment, "replies"): #moreComment instance
            replies = comment.comments() #get comment forest
            if verbose: print("fetching (" + totalFetched + " comments fetched total)")

        else:
            replies = comment.replies #get corresponding comment forest

        if not isinstance(comment, praw.models.MoreComments):
            if(comment.author == None):
                author = None
            else:
                author = comment.author.name
            body = comment.body
            treeCom = {"comment_id" : comment.id, "author" : author, "body" : body, "replies" : [], "score" : comment.score}
            parentNode["replies"].append(treeCom)#add information to parent node
        else:
            treeCom = parentNode

        for child in replies:#for each reply, no leaf comments
            self.getSubCommentsTree(child, treeCom, verbose=verbose, counter=counter)


    def getSubCommentslist(self, comment, verbose=True):
        allComments.append(comment)#add comment to list
        # get comment replies:
        if not hasattr(comment, "replies"): #moreComment instance
            replies = comment.comments() #get comment forest
            if verbose: print("fetching (" + str(len(allComments)) + " comments fetched total)")
        else:
            replies = comment.replies #get corresponding comment forest

        for child in replies:#for each reply, if replies exist, child instance of Comment
            self.getSubCommentslist(child, allComments, verbose=verbose)

    def getQandATreeForest(self, authorName):
        """get a forest of questions and answers (each answer has a list comment answer replies)

        Parameters
        ----------
        authorName : String
            the authors name (answer comments).

        Returns a forest of Q&A trees
        -------
        type
            dict

        """
        qaTreeForest = []
        for c in self.commentTree:
            replies = c["replies"]
            i = 0
            while((replies[i]["author"] != authorName) and (i < len(replies))):
                i += 1
            if i < len(replies):

                answerReplies = []
                for ar in replies[i]["replies"]:
                    answerReplies.append({"type":"answer_reply", "author":ar["author"], "body":ar["body"], "score":ar["score"]})

                answer = {"type":"answer", "author":authorName, "body":replies[i]["body"], "score":replies[i]["score"], "answers":answerReplies}
                qaTreeForest.append({"type":"question", "author":c["author"], "body":c["body"], "score": c["score"], "answer":answer})

        return qaTreeForest


    def compareQandA(self, qaTreeForest):
        """compares user in q&a tree forest.

        Parameters
        ----------
        qaTreeForest : list obtained by calling Post.getQandATreeForest
            list of dictionaries. Each dictionary has a question with a dictionary of answers.

        Returns a dictionary with an analysis of users.
        -------
        type
            dict.
        """
        for tree in qaTreeForest:
            print(tree["author"])

        pass


#####
##### functions (deprecated)
#####
def getSubComments(comment, allComments, verbose=True):
    allComments.append(comment)#add comment to list
    # get comment replies:
    if not hasattr(comment, "replies"): #moreComment instance
        replies = comment.comments() #get comment forest
        if verbose: print("fetching (" + str(len(allComments)) + " comments fetched total)")
    else:
        replies = comment.replies #get corresponding comment forest

    for child in replies:#for each reply, if replies exist, child instance of Comment
        getSubComments(child, allComments, verbose=verbose)



def getSubCommentsTree(comment, parentNode, verbose=True, counter=None):
    totalFetched = str(counter())
    if not hasattr(comment, "replies"): #moreComment instance
        replies = comment.comments() #get comment forest
        if verbose: print("fetching (" + totalFetched + " comments fetched total)")

    else:
        replies = comment.replies #get corresponding comment forest

    if not isinstance(comment, praw.models.MoreComments):
        if(comment.author == None):
            author = None
        else:
            author = comment.author.name
        body = comment.body
        treeCom = {"comment_id" : comment.id, "author" : author, "body" : body, "replies" : [], "score" : comment.score}
        parentNode["replies"].append(treeCom)#add information to parent node
    else:
        treeCom = parentNode

    for child in replies:#for each reply, no leaf comments
        getSubCommentsTree(child, treeCom, verbose=verbose, counter=counter)


def getAll(r, submissionId, verbose=True):
    """Gets All comments of a submission as a tree.

    Parameters
    ----------
    r : praw.Reddit
        a working and initialized instance of praw.Reddit
    submissionId : String
        Reddit submssion ID
    verbose : Boolean
        If verbose is true, indicates when comments are being fetched via the Praw API

    Returns
    -------
    type
        a list of dictionaries representing top comments and their children.
    """
    submission = r.submission(submissionId)
    comments = submission.comments #all top comments (as comment forest)
    tree = {"replies":[]}
    counter = _count()
    for comment in comments: #for all top comments, get subcomments
        getSubCommentsTree(comment, tree, verbose=verbose, counter=counter)
    return tree["replies"]


def topProfile(r, commentTree):
    userStats = {}

    for comm in commentTree:
        body = comm['body']
        commId = comm['comment_id']
        authorName = comm['author']

        if(authorName is not None) and (authorName != ""):
            print("user: -" + authorName + "-")
            userStats[authorName] = retrieve.userInfo.getSubmitedPosts(r.redditor(authorName), limit=100, listingType="new", verbose=False)

    return  userStats


def _count(start=0):
    c = start
    def increment():
        nonlocal c
        val = c
        c += 1
        return c
    return increment
