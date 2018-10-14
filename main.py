import sys
import praw
import json
import unittest
import retrieve.userInfo
import retrieve.retrievePost
from retrieve.retrievePost import Post
from retrieve.userInfo import User
import logging
import IPython
import importlib
import pandas

try:
    get_ipython
    importlib.reload(logging)  # workaround in Ipython console
except NameError:
    pass
logging.basicConfig(format='%(asctime)s | %(levelname)s : %(message)s',
                    level=logging.INFO, stream=sys.stdout)


class MainTest(unittest.TestCase):

    nameA = "JustNotGrunge"
    nameB = "Nickyjha"

    def setUp(self):
        self.r = praw.Reddit("afirsttest", user_agent="afirsttest V0.1 by u/CmonShowMe")
        self.postId = "7uypv6"
        self.post = Post(self.postId, self.r)
        self.userA = User(MainTest.nameA, self.r)
        self.userB = User(MainTest.nameB, self.r)

    def test_comp_AB(self):
        logger = logging.getLogger()

        commA = self.userA.getSubmitedComments()
        commB = self.userB.getSubmitedComments()

        logger.info("user A's comment posts" + str(commA))
        logger.info("user B's comment posts" + str(commB))
        logger.info("\ncomment posts" + str(self.userA.compare(self.userB)))

    def IGNORE_test_comp_top(self):
        logger = logging.getLogger()

        userCompDict = {}
        users = {}
        for u in self.post.commentTree:
            try:
                if u["author"] not in users:
                    users[u["author"]] = User(u["author"], self.r)
            except retrieve.userInfo.InvalidUserData:
                logger.info("invalid user name, ignoring this user")

        for u in users:
            for u1 in users:
                userCompDict[users[u].name] = {}
                userCompDict[users[u].name][users[u1].name] = users[u].compare(users[u1])

        def defaultJSON(x):
            print("calling default on {}".format(x))
            return x.__dict__

        # print(json.dumps(userCompDict, indent=2, default=defaultJSON))

    def test_comp_matrix(self):

        logger = logging.getLogger()

        users = []
        for u in self.post.commentTree:
            if u["author"] not in users:
                users.append(u["author"])

        userCompDict = self.post.compareUsers(users, limit=200)

        print(json.dumps(userCompDict, indent=2))
        dt = pandas.DataFrame.from_dict(userCompDict, orient='index')
        dt = dt.reindex(sorted(dt.columns), axis=1)
        print(dt)

if __name__ == "__main__":
    unittest.main()
    # print(sys.version)
    # r = praw.Reddit("afirsttest", user_agent="afirsttest V0.1 by u/CmonShowMe")
    # submId = "7uypv6"
    # p = Post(submId, r)
    # qa = p.getQandATreeForest("TriviaHawaii")
    # tp = Post.getTopProfile()
    # print(tp)

    # with open('qa.json', 'w') as fp:
    #     json.dump(qa, fp, indent=2)
