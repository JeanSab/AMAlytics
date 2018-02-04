#!/usr/bin/python3

import sys
import praw
import json

import retrieve.userInfo
import retrieve.retrievePost


if __name__ == "__main__":
    print(sys.version)
    r = praw.Reddit("afirsttest", user_agent="afirsttest V0.1 by u/CmonShowMe")
    submId = "7spdvg"
    subPostComms = retrieve.retrievePost.getAll(r, submId)

    with open('user_stat_test.json', 'w') as outfile:
        json.dump(subPostComms, outfile)






#submission = r.submission(submId)
#comments = submission.comments #all top comments (as comment forest)
#commentsList = [] #comments as list

#for comment in comments: #for all top comments, get subcomments
		#retrieve.retrievePost.getSubComments(comment, commentsList, verbose=True)

def topProfile(commentTree):
    userStats = {}

    for comm in commentTree:
        body = comm['body']
        commId = comm['comment_id']
        authorName = comm['author']

        if(authorName is not None) and (authorName != ""):
            print("user: -" + authorName + "-")
            userStats[authorName] = retrieve.userInfo.getSubmitedPosts(r.redditor(authorName), limit=100, listingType="new", verbose=False)

    with open('user_stat_test.json', 'w') as outfile:
        json.dump(userStats, outfile)


#for c in commentsList:
    #print(type(c))


#print(len(commentsList))
