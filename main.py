import sys
import praw
import json

import retrieve.userInfo
import retrieve.retrievePost
from retrieve.retrievePost import Post


if __name__ == "__main__":
    print(sys.version)
    r = praw.Reddit("afirsttest", user_agent="afirsttest V0.1 by u/CmonShowMe")
    submId = "7uypv6"
    p = Post(submId, r)
    qa = p.getQandATree("TriviaHawaii")

    with open('qa.json', 'w') as fp:
        json.dump(qa, fp)
