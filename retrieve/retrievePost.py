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
    
    # get comment replies:
    #allComments.append(comment)#list for verbose purpose
    totalFetched = str(counter())
    if not hasattr(comment, "replies"): #moreComment instance
        replies = comment.comments() #get comment forest
        if verbose: print("fetching (" + totalFetched + " comments fetched total)")

    else:
        replies = comment.replies #get corresponding comment forest

    treeRep = []
    if(type(comment) == praw.models.reddit.more.MoreComments):
        author = ""
        body = ""
    else:
        if(comment.author == None):
            author = None
        else:
            author = comment.author.name
        body = comment.body
            
    treeCom = {"comment_id" : comment.id, "author" : author, "body" : body, "replies" : treeRep}	
        
    parentNode.append(treeCom)#add information to parent node

    for child in replies:#for each reply, no leaf comments
        getSubCommentsTree(child, treeRep, verbose=verbose, counter=counter)


def getAll(r, submissionId, verbose=True):
    submission = r.submission(submissionId)
    comments = submission.comments #all top comments (as comment forest)
    tree = []
    counter = _count()
    for comment in comments: #for all top comments, get subcomments
        getSubCommentsTree(comment, tree, verbose=verbose, counter=counter)
    return tree


def _count(start=0):
    c = start
    def increment():
        nonlocal c
        val = c
        c += 1
        return c
    return increment




