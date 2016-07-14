class GnCalculate(object):
    def __init__(self, siz = 19):
        self.siz = siz
        self.ston = [[0 for x in range(26)] for y in range(26)]
        self.tmpbord = [[0 for x in range(26)] for y in range(26)]
        self.conflict = 0
        self.confmove = 0

    def findStoneBlock(self, colour, tmpcolour, pos, tmpsiz):
        movStack = []
        movStack.append(pos)
        breath = 0
        stonnum = 1
        while len(movStack):
            tmpmov = movStack.pop()
            tmpx = tmpmov / 100
            tmpy = tmpmov % 100

            if tmpx > 0 and self.tmpbord[tmpx - 1][tmpy] != tmpcolour:
                if self.ston[tmpx - 1][tmpy] == colour:
                    movStack.append(tmpmov - 100)
                    self.tmpbord[tmpx - 1][tmpy] = tmpcolour
                    stonnum += 1
                elif self.ston[tmpx - 1][tmpy] == 0:
                    breath += 1

            if tmpx < tmpsiz and self.tmpbord[tmpx + 1][tmpy] != tmpcolour:
                if self.ston[tmpx + 1][tmpy] == colour:
                    movStack.append(tmpmov + 100)
                    self.tmpbord[tmpx + 1][tmpy] = tmpcolour
                    stonnum += 1
                elif self.ston[tmpx + 1][tmpy] == 0:
                    breath += 1

            if tmpx > 0 and self.tmpbord[tmpx][tmpy - 1] != tmpcolour:
                if self.ston[tmpx][tmpy - 1] == colour:
                    movStack.append(tmpmov - 1)
                    self.tmpbord[tmpx][tmpy - 1] = tmpcolour
                    stonnum += 1
                elif self.ston[tmpx][tmpy - 1] == 0:
                    breath += 1

            if tmpx < tmpsiz and self.tmpbord[tmpx][tmpy + 1] != tmpcolour:
                if self.ston[tmpx][tmpy + 1] == colour:
                    movStack.append(tmpmov + 1)
                    self.tmpbord[tmpx][tmpy + 1] = tmpcolour
                    stonnum += 1
                elif self.ston[tmpx][tmpy + 1] == 0:
                    breath += 1

        return (breath, stonnum)   # finished findStoneBlock

    def configDropStone(self, colour, mov):
        tmpx = mov / 100
        tmpy = mov % 100
        if mov < 0:
            return 0
        if self.ston[tmpx][tmpy] > 0:
            return 0
        if self.conflict == 1 and mov == self.confmove:
            return 0

        tmpsiz = self.siz - 1
        if colour == 1:
            opcolour = 2
        else:
            opcolour = 1
        self.tmpbord = [[0 for x in range(26)] for y in range(26)]

        self.tmpbord[tmpx][tmpy] = 3
        self.ston[tmpx][tmpy] = colour

        lift = 0
        if tmpx > 0 and self.ston[tmpx - 1][tmpy] == opcolour:  # up
            self.tmpbord[tmpx - 1][tmpy] = 4
            tmpfind = self.findStoneBlock(opcolour, 4, mov - 100, tmpsiz)
            if tmpfind[0] == 0:
                lift += tmpfind[1]
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
            tmpfind = self.findStoneBlock(opcolour, 4, mov + 100, tmpsiz)
            if tmpfind[0] == 0:
                lift += tmpfind[1]
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
            tmpfind = self.findStoneBlock(opcolour, 4, mov - 1, tmpsiz)
            if tmpfind[0] == 0:
                lift += tmpfind[1]
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
            tmpfind = self.findStoneBlock(opcolour, 4, mov + 1, tmpsiz)
            if tmpfind[0] == 0:
                lift += tmpfind[1]
                for tmpi in range(self.siz):
                    for tmpj in range(self.siz):
                        if self.tmpbord[tmpi][tmpj] == 4:
                            self.tmpbord[tmpi][tmpj] = 5
            else:
                for tmpi in range(self.siz):
                    for tmpj in range(self.siz):
                        if self.tmpbord[tmpi][tmpj] == 4:
                            self.tmpbord[tmpi][tmpj] = 6

        tmpfind = self.findStoneBlock(colour, 3, mov, tmpsiz)
        if tmpfind[0] == 0 and lift == 0:
            self.ston[tmpx][tmpy] = 0
            return 0
        if lift == 1 and tmpfind[1] == 1:
            if tmpx > 0 and self.tmpbord[tmpx - 1][tmpy] == 5:
                self.ston[tmpx - 1][tmpy] = 0
                self.confmove = (tmpx - 1) * 100 + tmpy
            if tmpx < tmpsiz and self.tmpbord[tmpx + 1][tmpy] == 5:
                self.ston[tmpx + 1][tmpy] = 0
                self.confmove = (tmpx + 1) * 100 + tmpy
            if tmpy > 0 and self.tmpbord[tmpx][tmpy - 1] == 5:
                self.ston[tmpx][tmpy - 1] = 0
                self.confmove = tmpx * 100 + tmpy - 1
            if tmpy < tmpsiz and self.tmpbord[tmpx][tmpy + 1] == 5:
                self.ston[tmpx][tmpy + 1] = 0
                self.confmove = tmpx * 100 + tmpy + 1
            self.conflict = 1
            return 1
        if lift > 0:
            self.conflict = 0
            for tmpi in range(0, self.siz):
                for tmpj in range(0, self.siz):
                    if self.tmpbord[tmpi][tmpj] == 5:
                        self.ston[tmpi][tmpj] = 0
            return 2
        self.conflict = 0
        return 3
        # finished configDropStone


    def printbord(self):
        for x in range(self.siz):
            for y in range(self.siz):
                print self.ston[x][y],
            print

if __name__ == "__main__":
    colour = 1
    App = GnCalculate(19)
    App.printbord()
    while True:
        if colour == 1:
            move = input("Black: ")
        else:
            move = input("White: ")
        App.printbord()
        if colour == 1:
            colour = 2
        else:
            colour = 1
