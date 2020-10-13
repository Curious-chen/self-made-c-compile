class Sentence_:
    def __init__(self, id, op, n1, n2, res):
        self.id = id
        self.op = op
        self.n1 = n1
        self.n2 = n2
        self.res = res

    def setRes(self, out):
        self.res = out
