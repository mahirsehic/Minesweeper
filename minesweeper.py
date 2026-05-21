import random
import os

limit = []

class Cell:
    def __init__(self, position, typee = 0):
        self.position = position #maybe drow position instead of O
        self.typee = typee # -1 - bomb, 0-blank, >0-number
        self.state = 0 # 0 - unrevealed, 1 - revealed, 2 - flagged

    def increment(self):
        if self.typee != -1:
            self.typee += 1

    def setBomb(self):
        self.typee = -1

    def revealed(self):
        self.state = 1

    def flagged(self):
        if self.state == 0:
            self.state = 2
        elif self.state == 2:
            self.state = 0

def surroundingArea(position, width):
    global limit
    positions = []
    left = True
    right = True
    for x in limit:
        if position == x:
            left = False
            break
        elif position == x - 1:
            right = False
            break
        
    if position == width * len(limit) - 1:
        right = False
        
    if left:
        positions.append(position - width - 1)
        positions.append(position - 1)
        positions.append(position + width - 1)
        
    if right:
        positions.append(position - width + 1)
        positions.append(position + 1)
        positions.append(position + width + 1)

    positions.append(position - width)
    positions.append(position + width)
    
    return positions

def cascade(cells, position, width):
    for x in surroundingArea(position, width):
        if x < 0:
            continue
        try:
            if cells[x].state == 0:
                cells[x].revealed()
                if cells[x].typee == 0:
                    cascade(cells, x, width)
        except:
            pass

def calculate(cells, nBombs, size, width):
    bombs = []
    for x in range(size):
        cells.append(Cell(x))
        
    for x in range(nBombs):
        bomb = random.randrange(size)
        while(bomb in bombs):
            bomb = random.randrange(size)
        bombs.append(bomb)
        cells[bomb].setBomb()
        for x in surroundingArea(bomb, width):
            if x < 0:
                continue
            try:
                cells[x].increment()
            except:
                pass

def action(cells, option, choice, width):
    if option == 'r':
        if cells[choice].typee == 0:
            cascade(cells, choice, width)
        cells[choice].revealed()
    else:
        cells[choice].flagged()

def draw(cells, height, width, nBombs = 10):
    if nBombs != -3:
        os.system("cls")
    unrevealed = 0
    cWidth = 0
    result = 2
    for cell in cells:
        if nBombs == -1 and cell.typee == -1:
            cell.state = 1
        if cell.state == 1 or nBombs == -2:
            if cell.typee == -1:
                print("X", end="")
                result = 1 #Game Over
            elif cell.typee == 0:
                print(" ", end="")#Draw Blank
            else:
                print(cell.typee, end="")#Draw Number from cell.typee
                
        elif cell.state == 0:
            print("O", end="")#draw unrevealed
            unrevealed += 1
            
        elif cell.state == 2:
            print("F", end="")#Draw Flag
            unrevealed += 1
            
        cWidth += 1
        if cWidth == width:
            print()
            cWidth = 0
            
            
    if unrevealed == nBombs:
        result = 0 #Win

    if nBombs == -2:
        print("-" * width)
        draw(cells, height, width, -3)
    
    return result 

def main():
    width = 15
    height = 10
    nBombs = 30
    cells = []
    for x in range(height):
        y = width * x
        limit.append(y)
    calculate(cells, nBombs, width*height, width) #width*height if cell:position
    result = 2
    draw(cells, height, width, nBombs)
    while result == 2:
        option = input("Option (f - flag, r - reveal, s - settings, x - peek)\n")
        while option != 'r' and option != 'f' and option != 's' and option != 'x':
            option = input("Option (f - flag, r - reveal, s - settings, x - peek)\n")
        if option == 's':
            print(f"Width (previous: {width})\n")
            width = int(input())
            print(f"Height (previous: {height})\n")
            height = int(input())
            print(f"Number of bombs (previous: {nBombs})\n")
            nBombs = int(input())
            cells.clear()
            calculate(cells, nBombs, width*height, width)
            draw(cells, height, width, nBombs)
            continue
        elif option == 'x':
            draw(cells, height, width, -2)
            continue
        choice = int(input("Choice ([0 - {}])\n".format(width*height-1)))
        while choice < 0 or choice >= width*height:
            choice = int(input("Choice ([0 - {}])\n".format(width*height-1)))
        action(cells, option, choice, width)
        result = draw(cells, height, width, nBombs)
        
    if result == 0:
        print("You Won")
    else:
        print("You Lost")
    draw(cells, height, width, -1)
    input()

main()
