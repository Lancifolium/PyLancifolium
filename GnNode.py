class GnNode(object):
    def __init__(self, parent):
        self.parent = parent
        self.next = None
        self.nxt = None  # []
        self.stoneProp = 0
        self.mov = -1
        self.addblacks = None  # []
        self.addwhites = None  # []
        self.labels = None  # {}
        self.comment = None  # string
        self.nodename = None  # string

    def printbase(self):
        print "[", self.mov, "]"
