
class SgfStruct(object):
    def __init__(self, siz = 19):
        self.siz = siz

        self.ston = [[0 for x in range(26)] for y in range(26)]
        self.tmpbord = [[0 for x in range(26)] for y in range(26)]
        self.root = None

        self.filereading = None
        self.reader = '0'
        self.deep = 0
        self.curNode = None
        self.tmpNode = None
        self.branchStack = None

        self.conflict = 0
        self.confmove = 0

    def findStoneBlock(self, colour, tmpcolour, pos, tmpsiz):
        movStack = []
        movStack.append(pos)
        breath = 0
        while len(movStack):
            tmpmov = movStack.pop()
            tmpx = tmpmov / 100
            tmpy = tmpmov % 100

            if tmpx > 0 and self.tmpbord[tmpx - 1][tmpy] != tmpcolour:
                if self.ston[tmpx - 1][tmpy] == colour:
                    movStack.append(tmpmov - 100)
                    self.tmpbord[tmpx - 1][tmpy] = tmpcolour
                elif self.ston[tmpx - 1][tmpy] == 0:
                    breath += 1

            if tmpx < tmpsiz and self.tmpbord[tmpx + 1][tmpy] != tmpcolour:
                if self.ston[tmpx + 1][tmpy] == colour:
                    movStack.append(tmpmov + 100)
                    self.tmpbord[tmpx + 1][tmpy] = tmpcolour
                elif self.ston[tmpx + 1][tmpy] == 0:
                    breath += 1

            if tmpx > 0 and self.tmpbord[tmpx][tmpy - 1] != tmpcolour:
                if self.ston[tmpx][tmpy - 1] == colour:
                    movStack.append(tmpmov - 1)
                    self.tmpbord[tmpx][tmpy - 1] = tmpcolour
                elif self.ston[tmpx][tmpy - 1] == 0:
                    breath += 1

            if tmpx < tmpsiz and self.tmpbord[tmpx][tmpy + 1] != tmpcolour:
                if self.ston[tmpx][tmpy + 1] == colour:
                    movStack.append(tmpmov + 1)
                    self.tmpbord[tmpx][tmpy + 1] = tmpcolour
                elif self.ston[tmpx][tmpy + 1] == 0:
                    breath += 1

        return breath   # finished findStoneBlock

    def configDropStone(self, colour, mov):
        tmpsiz = self.siz - 1
        if colour == 1:
            opcolour = 2
        else:
            opcolour = 1
        self.tmpbord = [[0 for x in range(26)] for y in range(26)]
        tmpx = mov / 100
        tmpy = mov % 100
        self.tmpbord[tmpx][tmpy] = 3
        self.ston[tmpx][tmpy] = colour

        lift = 0
        if tmpx > 0 and self.ston[tmpx - 1][tmpy] == opcolour:  # up
            self.tmpbord[tmpx - 1][tmpy] = 4
            if self.findStoneBlock(opcolour, 4, mov - 100, tmpsiz) == 0:
                lift += 1
                for tmpi in range(self.siz):
                    for tmpj in range(self.siz):
                        if self.tmpbord[tmpi][tmpj] == 4:
                            self.tmpbord[tmpi][tmpj] = 5
            else:
                for tmpi in range(self.siz):
                    for tmpj in range(self.siz):
                        if self.tmpbord[tmpi][tmpj] == 4:
                            self.tmpbord[tmpi][tmpj] = 6

        if tmpx < tmpsiz and self.ston[tmpx - 1][tmpy] == opcolour and self.tmpbord[tmpx + 1][tmpy] != 5 \
                and self.tmpbord[tmpx + 1][tmpy] != 6:  # down
            self.tmpbord[tmpx + 1][tmpy] = 4
            if self.findStoneBlock(opcolour, 4, mov + 100, tmpsiz) == 0:
                lift += 1
                for tmpi in range(self.siz):
                    for tmpj in range(self.siz):
                        if self.tmpbord[tmpi][tmpj] == 4:
                            self.tmpbord[tmpi][tmpj] = 5
            else:
                for tmpi in range(self.siz):
                    for tmpj in range(self.siz):
                        if self.tmpbord[tmpi][tmpj] == 4:
                            self.tmpbord[tmpi][tmpj] = 6

        if tmpy > 0 and self.ston[tmpx][tmpy - 1] == opcolour and self.tmpbord[tmpx][tmpy - 1] != 5 \
                and self.tmpbord[tmpx][tmpy - 1] != 6:  # left
            self.tmpbord[tmpx][tmpy - 1] = 4
            if self.findStoneBlock(opcolour, 4, mov - 1, tmpsiz) == 0:
                lift += 1
                for tmpi in range(self.siz):
                    for tmpj in range(self.siz):
                        if self.tmpbord[tmpi][tmpj] == 4:
                            self.tmpbord[tmpi][tmpj] = 5
            else:
                for tmpi in range(self.siz):
                    for tmpj in range(self.siz):
                        if self.tmpbord[tmpi][tmpj] == 4:
                            self.tmpbord[tmpi][tmpj] = 6

        if tmpy < tmpsiz and self.ston[tmpx][tmpy + 1] == opcolour and self.tmpbord[tmpx][tmpy + 1] != 5 \
                and self.tmpbord[tmpx][tmpy + 1] != 6:  # right
            self.tmpbord[tmpx][tmpy + 1] = 4
            if self.findStoneBlock(opcolour, 4, mov + 1, tmpsiz) == 0:
                lift += 1
                for tmpi in range(self.siz):
                    for tmpj in range(self.siz):
                        if self.tmpbord[tmpi][tmpj] == 4:
                            self.tmpbord[tmpi][tmpj] = 5
            else:
                for tmpi in range(self.siz):
                    for tmpj in range(self.siz):
                        if self.tmpbord[tmpi][tmpj] == 4:
                            self.tmpbord[tmpi][tmpj] = 6

        if self.findStoneBlock(colour, 3, mov, tmpsiz) == 0 and lift == 0:
            self.ston[tmpx][tmpy] = 0
            return 0
        elif lift > 0:
            return 1
        else:
            return 2
        # finished configDropStone

    def liftstones(self, lift):
        if lift == 1:
            cont = 0
            for tmpi in range(self.siz):
                for tmpj in range(self.siz):
                    if self.tmpbord[tmpi][tmpj] == 5:
                        self.ston[tmpi][tmpj] = 0
                        lift = tmpi * 100 + tmpj
                        cont += 1
            if cont == 1:
                self.conflict = 1
                self.confmove = lift
        return 1

    def openfile(self, filename):
        self.filereading = open(filename, "r")
        if self.filereading != Node:
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
            tmpnum.append(readr)
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
            if tmpx >= 0 and tmpx < self.siz and tmpy >= 0 and tmpy < self.siz:
                step = self.configDropStone(colour, tmpx + tmpy * 100)
                self.liftstones(step)
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


    def configRoot(self):
        operate = ''
        self.reader = self.filereading.read(1)
        while self.reader != ';' and self.reader != '(' and self.reader != ')':
            while self.iswhite(self.reader):
                self.reader = self.filereading.read(1)
            tmpi = 0
            while self.reader.isalpha():
                operate.append(self.reader)
                self.reader = self.filereading.read(1)
            operate = operate.upper()
            while self.reader and self.reader != '[':
                self.reader = self.filereading.read(1)
            if not self.reader:
                break
            print operate + " |OPERATE|"

            if operate is "LB":
                self.dealAddStones()
