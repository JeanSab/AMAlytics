#!/usr/bin/python3
import praw


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


def _count(start=0):
    c = start
    def increment():
        nonlocal c
        val = c
        c += 1
        return c
    return increment
