

class Test:

    def __init__(self):
        pass

    def test(self):
        self.a = "a"
        self.b = "b"

        if hasattr(self, "a"):
            print("we have a")
        else:
            print("we don't have a")

        if not hasattr(self, "c"):
            print("no c")
            self.c = "c"
        else:
            print("yes c")


if __name__ == '__main__':
    t = Test()
    t.test()
    t.test()
