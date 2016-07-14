from GnNode import GnNode


class SgfStruct(object):
    def __init__(self, siz = 19):
        self.siz = siz

        self.root = None

        self.filereading = None
        self.reader = '0'

        self.curNode = None
        self.tmpNode = None
        self.branchStack = []

    def openfile(self, filename):
        self.filereading = open(filename, "r")
        if self.filereading is not None:
            return 1
        else:
            return 0

    def iswhite(self, alp):
        if alp == ' ' or alp == '\n' or alp == '\t':
            return True
        return False

    def dealSize(self):
        self.reader = self.filereading.read(1)
        tmpnum = ''
        while self.reader.isdigit():
            tmpnum += self.reader
            self.reader = self.filereading.read(1)
        self.siz = int(tmpnum)
        if self.siz < 4:
            self.siz = 4
        if self.siz > 26:
            self.siz = 26
        self.reader = self.filereading.read(1)

    def dealAddStones(self, tmpnode, colour):
        if colour == 0:
            return
        elif colour != 1:
            colour = 2

        while self.reader is '[':
            tmpx = ord(self.filereading.read(1).upper()) - ord('A')
            tmpy = ord(self.filereading.read(1).upper()) - ord('A')
            if 0 <= tmpx < self.siz and 0 <= tmpy < self.siz:
                tmpmove = tmpx * 100 + tmpy
                if colour == 1:
                    if tmpnode.addblacks is None:
                        tmpnode.addblacks = []
                        tmpnode.addblacks.append(tmpmove)
                    elif tmpmove not in tmpnode.addblacks:
                        tmpnode.addblacks.append(tmpmove)
                elif colour == 2:
                    if tmpnode.addwhites is None:
                        tmpnode.addwhites = []
                        tmpnode.addwhites.append(tmpmove)
                    elif tmpmove not in tmpnode.addwhites:
                        tmpnode.addwhites.append(tmpmove)
            self.reader = self.filereading.read(1) # get ']'
            self.reader = self.filereading.read(1) # get '['

    def dealMove(self, tmpnode, colour):
        self.reader = self.filereading.read(1)
        while self.reader and not self.reader.isalpha():
            self.reader = self.filereading.read(1)
        tmpx = ord(self.reader.upper()) - ord('A')
        self.reader = self.filereading.read(1)
        tmpy = ord(self.reader.upper()) - ord('A')
        if not self.reader:
            return
        tmpnode.mov = tmpx * 100 + tmpy
        tmpnode.stoneProp = colour
        self.reader = self.filereading.read(1)  # get ']'
        self.reader = self.filereading.read(1)  # get '['

    def dealCommentNodename(self, tmpnode, tmpkind):
        self.reader = self.filereading.read(1)  # abandon '['
        tmpsave = '\0'
        buff = ''
        while self.reader != ']' or tmpsave == '\\':
            if tmpsave == '\\':
                if self.reader == 'n':
                    buff = buff[0 : len(buff) - 1] + '\n'
                elif self.reader == 't':
                    buff = buff[0 : len(buff) - 1] + '\t'
                elif self.reader == '[' or self.reader == ']' or self.reader == '\\':
                    buff = buff[0 : len(buff) - 1] + self.reader
                else:
                    buff += self.reader
                tmpsave = self.reader
            else:
                buff += self.reader
                tmpsave = self.reader

            self.reader = self.filereading.read(1)

        if tmpkind == 1:
            tmpnode.comment = buff
        else:
            tmpnode.nodename = buff
        self.reader = self.filereading.read(1)  # abandon ']'

    def dealLabels(self, tmpnode, form):
        if tmpnode.labels is None:
            tmpnode.labels = []
        tmppool = []

        print self.reader, "================="

        while self.reader == '[':
            tmplabel = ord(self.filereading.read(1).upper()) - ord('A')
            tmplabel = tmplabel * 100 + ord(self.filereading.read(1).upper()) - ord('A')
            tmppool.append(tmplabel)
            self.reader = self.filereading.read(1)
            self.reader = self.filereading.read(1)
            print tmppool  # =============

        if form == 0:
            for tmpi in range(0, len(tmppool)):
                tmppool[tmpi] += (ord('A') + tmpi) * 10000
        elif form in [1, 2, 3, 4]:
            for tmpi in range(0, len(tmppool)):
                tmppool[tmpi] += 10000 * form

        tmpnode.labels.extend(tmppool)

    def configNode(self, currentNode):
        self.reader = self.filereading.read(1)
        while self.reader != ';' and self.reader != '(' and self.reader != ')':
            operate = ""
            while self.iswhite(self.reader):
                self.reader = self.filereading.read(1)
            while self.reader.isalpha():
                operate += self.reader
                self.reader = self.filereading.read(1)
            operate = operate.upper()
            while self.reader and self.reader != '[':
                self.reader = self.filereading.read(1)
            if not self.reader:
                break
            print operate, "|OPERATE|", self.reader

            if operate == "LB":
                self.dealLabels(currentNode, 0)
            elif operate == "TR":
                self.dealLabels(currentNode, 1)
            elif operate == "SQ":
                self.dealLabels(currentNode, 2)
            elif operate == "MA":
                self.dealLabels(currentNode, 3)
            elif operate == "CR":
                self.dealLabels(currentNode, 4)
            elif operate == "C":
                self.dealCommentNodename(currentNode, 1)
            elif operate == "N":
                self.dealCommentNodename(currentNode, 2)
            elif operate == "AB":
                self.dealAddStones(currentNode, 1)
            elif operate == "AW":
                self.dealAddStones(currentNode, 2)
            elif operate == "SZ":
                self.dealSize()
            elif operate == "B":
                self.dealMove(currentNode, 1)
            elif operate == "W":
                self.dealMove(currentNode, 2)
            else:
                while self.reader and self.reader != ']':
                    self.reader = self.filereading.read(1)
                self.reader = self.filereading.read(1)  # abandon

            while self.iswhite(self.reader):
                self.reader = self.filereading.read(1)
            # finished while loop for ';' or '('
        # finished configNode

    def configManual(self, filename):
        if not self.openfile(filename=filename):
            return
        if self.root is not None:
            return
        self.root = GnNode(None)
        self.branchStack = []

        self.reader = self.filereading.read(1)
        while self.reader and self.reader != '(':
            self.reader = self.filereading.read(1)
        while self.reader and self.reader != ';':
            self.reader = self.filereading.read(1)
        self.configNode(self.root)
        self.curNode = self.root

        while True:
            if self.reader == ';':
                tmpNode = self.curNode
                self.curNode = GnNode(tmpNode)
                tmpNode.next = self.curNode
                self.configNode(self.curNode)
            elif self.reader == '(':
                tmpNode = self.curNode
                self.curNode = GnNode(tmpNode)
                if tmpNode.nxt is None:
                    tmpNode.nxt = []
                tmpNode.nxt.append(self.curNode)
                self.branchStack.append(tmpNode)
                self.reader = self.filereading.read(1)
                while self.reader and self.reader != ';' and self.reader != '(' and self.reader != ')':
                    self.reader = self.filereading.read(1)
                if self.reader == ';':
                    self.configNode(self.curNode)
            elif self.reader == ')':
                if len(self.branchStack) == 0:
                    print "Finished Reading Manual. "
                    break
                else:
                    self.curNode = self.branchStack.pop()
                    self.reader = self.filereading.read(1)
                    while self.reader and self.reader != ';' and self.reader != '(' and self.reader != ')':
                        self.reader = self.filereading.read(1)
            if not self.reader:
                break
        # finished config

    def reverse(self, deep, tmpnode):
        if tmpnode is None:
            return
        tmpnode.printbase()
        self.reverse(deep, tmpnode.next)

        if tmpnode.nxt is not None:
            if len(tmpnode.nxt) > 0:
                for tmpi in range(0, len(tmpnode.nxt)):
                    for x in range(0, deep):
                        print "  ",
                    print "\n|", deep, "|"
                    self.reverse(deep, tmpnode.nxt[tmpi])

    def printfManual(self):
        deep = 0
        print "\n"
        self.reverse(deep, self.root)

if __name__ == '__main__':
    manual = SgfStruct()
    filename = input("Insert filename: ")
    manual.configManual(filename)
    manual.printfManual()
