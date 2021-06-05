import os
import random

class Square:
  def __init__(self):
    self.isBomb = False
    self.isHidden = True
    self.isFlagged = False
    self.exploded = False
    self.adjacentBombs = 0
    self.emojis = {"1":" 1", "2":" 2", "3":" 3", "4":" 4", "5":" 5", "6":" 6", "7":" 7", "8":" 8", "9":" 9", "0":u"⬛"}

  def setAdjacentBombs(self, num):
    self.adjacentBombs = num

  def click(self):
    self.isHidden = False

  def toggleFlag(self):
    self.isFlagged = not self.isFlagged

  def __str__(self):
    return u"💥" if self.exploded else u"🚩" if self.isFlagged else u"⬜" if self.isHidden else u"💣" if self.isBomb else self.emojis[str(self.adjacentBombs)]

class Board:
  def __init__(self, width, height, bombCount):
    if bombCount > (width*height)-1:
      print("Invalid bomb count, cannot produce board with no usable spaces.")
      exit(0)

    if width>26 or height>26 or width<5 or height<5:
      print("Invalid grid size, size should be within 26x26 to 5x5.")
      exit(0)

    if bombCount < 0:
      print("Invalid bomb count, cannot have negative bombs.")
      exit(0)

    self.isDead = False
    self.won = False
    self.width = width
    self.height = height
    self.bombCount = bombCount
    self.blankStage()

  def print(self):
    os.system("cls")

    print("  " + ' '.join([chr(c) for c in range(ord("A"), ord("A")+self.width)]))
    printable = [u"".join([str(y) for y in x]) for x in self.stage]
    for i in range(len(printable)):
      print(chr(ord("A") + i), end="")
      if self.won:
        print(printable[i].replace(u"⬜", u"✨"), end=" ")
      else:
        print(printable[i], end=" ")
      print(chr(ord("A") + i))
    print("  " + ' '.join([chr(c) for c in range(ord("A"), ord("A")+self.width)]))

  def toggleFlag(self, x, y):
    if self.stage[y][x].isHidden:
      self.stage[y][x].toggleFlag()

  def click(self, x, y):
    square = self.stage[y][x]
    if square.isHidden and not square.isFlagged:
      square.click()
      if square.isBomb:
        square.exploded = True
        self.showAllBombs()
        return -1
    if square.adjacentBombs == 0:
      square.isHidden = True
      self.expandBlankIsland(x, y)
    return 0

  def showAllBombs(self):
    for row in self.stage:
      for square in row:
        if square.isBomb:
          square.isHidden = False
          square.isFlagged = False

  def populate(self, clickX, clickY):
    if self.bombCount == (self.width*self.height)-1:
      for row in self.stage:
        for square in row:
          if square.isBomb:
            square.isBomb = True
      self.stage[clickY][clickX].isBomb = False

    else:
      bombsLeft = self.bombCount
      while bombsLeft>0:
        randX = random.randint(0, self.width-1)
        randY = random.randint(0, self.height-1)

        if not self.stage[randY][randX].isBomb and (clickX != randX and clickY != randY):
          self.stage[randY][randX].isBomb = True

          bombsLeft-=1

    for x in range(self.width):
      for y in range(self.height):
        square = self.stage[y][x]
        if not square.isBomb:
          adjacentBombs = sum([1 for i in range(9) if self.width>(x + ((i%3)-1))>=0 and self.height>(y + ((i//3)-1))>=0 and self.stage[y + ((i//3)-1)][x + ((i%3)-1)].isBomb])
          square.adjacentBombs = adjacentBombs

    if self.stage[clickY][clickX].adjacentBombs != 0:
      self.blankStage()
      self.populate(clickX, clickY)

  def blankStage(self):
    self.stage = [[Square() for x in range(self.width)] for y in range(self.height)]

  def expandBlankIsland(self, posX, posY):
    if self.stage[posY][posX].isHidden == False:
      return None

    self.stage[posY][posX].isHidden = False

    # Check orthogonally adjacent squares
    if not (posY - 1 < 0):
      if not (self.stage[posY-1][posX].adjacentBombs != 0):
        self.expandBlankIsland(posX, posY-1)
      else:
        self.stage[posY-1][posX].isHidden = False
    if not (posX + 1 > (self.width-1)):
      if not (self.stage[posY][posX+1].adjacentBombs != 0):
        self.expandBlankIsland(posX+1, posY)
      else:
        self.stage[posY][posX+1].isHidden = False
    if not (posY + 1 > (self.height-1)):
      if not (self.stage[posY+1][posX].adjacentBombs != 0):
        self.expandBlankIsland(posX, posY+1)
      else:
        self.stage[posY+1][posX].isHidden = False
    if not (posX - 1 < 0):
      if not (self.stage[posY][posX-1].adjacentBombs != 0):
        self.expandBlankIsland(posX-1, posY)
      else:
        self.stage[posY][posX-1].isHidden = False

    # Check diaogonally adjacent squares
    if not (posY - 1 < 0) and not (posX + 1 > (self.width-1)):
      if not (self.stage[posY-1][posX+1].adjacentBombs != 0):
        self.expandBlankIsland(posX+1, posY-1)
      else:
        self.stage[posY-1][posX+1].isHidden = False
    if not (posX + 1 > (self.width-1)) and not (posY + 1 > (self.height-1)):
      if not (self.stage[posY+1][posX+1].adjacentBombs != 0):
        self.expandBlankIsland(posX+1, posY+1)
      else:
        self.stage[posY+1][posX+1].isHidden = False
    if not (posY + 1 > (self.height-1)) and not (posX - 1 < 0):
      if not (self.stage[posY+1][posX-1].adjacentBombs != 0):
        self.expandBlankIsland(posX-1, posY+1)
      else:
        self.stage[posY+1][posX-1].isHidden = False
    if not (posX - 1 < 0) and not (posY - 1 < 0):
      if not (self.stage[posY-1][posX-1].adjacentBombs != 0):
        self.expandBlankIsland(posX-1, posY-1)
      else:
        self.stage[posY-1][posX-1].isHidden = False

  def checkIfWon(self):
    for line in self.stage:
      for square in line:
        if not square.isBomb:
          if square.isHidden:
            return False
    return True

board = Board(*list(map(int, input("Width Height BombCount\n> ").split())))
firstClick = True

while not board.isDead:
  board.print()
  action, posX, posY = input("\n(C)lick/(F)lag column row\n> ").lower().split()
  if posX.isalpha():
    posX = 25-(ord("z")-ord(posX))
  if posY.isalpha():
    posY = 25-(ord("z")-ord(posY))

  print(posX, posY)

  if action == "c":
    if firstClick:
      board.populate(posX, posY)
      # board.showAllBombs()
      firstClick = False
    result = board.click(posX, posY)

    if result == -1:
      board.print()
      board.isDead = True
    else:
      if board.checkIfWon():
        board.won = True
        board.print()
        print("Well done you won!")
        exit(0)

  elif action == "f":
    board.toggleFlag(posX, posY)


print("Game Over")