#!/usr/bin/python3

import praw
import json

import retrieve.userInfo
import retrieve.retrievePost





def getAllComments():

	submId = "7ss950"
	r = praw.Reddit("afirsttest", user_agent="afirsttest V0.1 by u/CmonShowMe")
	amaSubmission = r.submission(submId)
	allComments = retrieve.retrievePost.getAll(r, submId)

	#with open('result.json', 'w') as fp:
	#	json.dump(allComments, fp)



getAllComments()

#print(type(amaSubmission.comments[0]))
#print(dir(amaSubmission.comments[0]))



#submission = r.submission(submId)
#comments = submission.comments #all top comments (as comment forest)
#commentsList = [] #comments as list

#for comment in comments: #for all top comments, get subcomments
		#retrieve.retrievePost.getSubComments(comment, commentsList, verbose=True)




#for c in commentsList:
    #print(type(c))
    

#print(len(commentsList))
