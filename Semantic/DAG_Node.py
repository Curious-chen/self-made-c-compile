class DAG:
    def __init__(self, id, val, value, leftchild=None, rightchild=None):
        self.id = id
        self.val = val
        self.value = []
        self.leftchild = leftchild
        self.rightchild = rightchild
        self.add_value(value)

    def add_value(self, value):
        if value != None:
            self.value.append(value)
