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


def getSubCommentsTree(comment, allComments, parentNode, verbose=True):
  # get comment replies:
  allComments.append(comment)#list for verbose purpose
  if not hasattr(comment, "replies"): #moreComment instance
    replies = comment.comments() #get comment forest
    if verbose: print("fetching (" + str(len(allComments)) + " comments fetched total)")
  else:
    replies = comment.replies #get corresponding comment forest

  treeRep = []
  treeCom = {"comment" : comment, "replies" : treeRep}
  parentNode.append(treeCom)#add information to parent node

  for child in replies:#for each reply
    getSubCommentsTree(child, allComments, treeRep, verbose=verbose)



def getAll(r, submissionId, verbose=True):
  submission = r.submission(submissionId)
  comments = submission.comments #all top comments (as tree)
  commentsList = [] #comments as list
  tree = []
  for comment in comments: #for all top comments, get subcomments
    getSubCommentsTree(comment, commentsList, tree, verbose=verbose)
  return tree



username = 'afirsttest'
userAgent = "MyAppName/0.1 by " + username
clientId = 'aRFvr_zLw5DU9g'
clientSecret = "XJDn3Swh5qSJWVNA2xes1oi0_7U"

r = praw.Reddit(user_agent=userAgent, client_id=clientId, client_secret=clientSecret)

res = getAll(r, "7s85ar")

print(res)
