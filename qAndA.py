import praw
import userInfo

class QAndA(object):
    """docstring for ."""
    def __init__(self, qAndATree, load=True):
        self.qAndATree = qAndATree
        if load is True:
            self.load()

    def load(self):
        self.Qposter = praw.Redditor(self.qAndATree["author"])
        self.Aposter = praw.Redditor(self.qAndATree["answer"]["author"])
        self.ARposters = []

        for arp in qAndATree["answer"]["answers"]:
            self.ARposters.push(praw.Redditor(arp["author"]))

    def analyze(self):
        pass

    def posterSimilarities(self):
        pass

    def posterSimilaritiesByVote(self):
        pass

    
