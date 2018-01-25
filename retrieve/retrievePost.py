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
	
	
	if(type(comment) == praw.models.reddit.more.MoreComments):
		treeCom = {"comment_id" : comment.id, "author" : "", "body" : "", "replies" : treeRep}
	else:
		if(comment.author == None):
			author = None
		else:
			author = comment.author.name
			
		treeCom = {"comment_id" : comment.id, "author" : author, "body" : comment.body, "replies" : treeRep}
		
		
	parentNode.append(treeCom)#add information to parent node

	for child in replies:#for each reply, no leaf comments
		getSubCommentsTree(child, allComments, treeRep, verbose=verbose)


def getAll(r, submissionId, verbose=True):
	submission = r.submission(submissionId)
	comments = submission.comments #all top comments (as comment forest)
	commentsList = [] #comments as list
	tree = []
	for comment in comments: #for all top comments, get subcomments
		getSubCommentsTree(comment, commentsList, tree, verbose=verbose)
	return tree




