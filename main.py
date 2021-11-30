from functools import partial
import tkinter
from collections import defaultdict
from PIL import Image, ImageDraw, ImageTk, ImageFont
import random
import time
import numpy as np
import threading
import sys
#random.seed(42)# i need to test the algorithms on the same boards to check if they work consistently

# i have used the walrus operator in this script so your python version must be higher from 3.8
assert sys.version_info > (3, 8), "Use Python 3.8 or newer"


moveDelay = 0.1   # s
specsUpdate = 100 # ms

class Graph:
    def __init__(self, board):
        self.board = board

        self.visitedNodes = 0
        self.activeNodes = 0
        self.idsDepth = 0

    def listToStr(self, theList):
        return "".join([str(i) for i in theList])
  
    def strToList(self, theStr):
        return [int(i) for i in theStr]

    def getChildNodes(self, board): 
        # sourcery skip: inline-immediately-returned-variable, list-comprehension
        childList = []
        for possibleMove in self.allPossibleMoves(board):
            childList.append((self.listToStr(self.swapTiles(possibleMove, board)), possibleMove))
        return childList
      
    def bfs(self): # Breath-first search
        visited = [self.listToStr(self.board)]
        queue = [(self.listToStr(self.board), "")]
        currentNode, path = queue[0]
        if currentNode == "012345678":
                return path

        while queue:
            currentNode, path = queue.pop(0)

            self.visitedNodes = len(visited) # to show these stats in the tkinter
            self.activeNodes = len(queue)

         

            for child, move in self.getChildNodes(self.strToList(currentNode)):
                
                move = path + str(move)

                if child not in visited:
                    visited.append(child)
                    queue.append((child, move))
                    if child == "012345678":
                        return move
        return ""

    def ucs(self): # Uniform- cost search
        # https://www.geeksforgeeks.org/uniform-cost-search-dijkstra-for-large-graphs/
        visited = [self.listToStr(self.board)]
        queue = [(self.listToStr(self.board), "")]
        currentNode, path = queue[0]
        if currentNode == "012345678":
                return path

        while queue:
            currentNode, path = queue.pop(0)

            self.visitedNodes = len(visited) # to show these stats in the tkinter
            self.activeNodes = len(queue)

            # My cost function is the total length of path.
            # This is totally unnecessary because all the step costs are equal,
            # This is already equal to BFS, but i will add for the sake of the 
            # implementation and it will slow the Uniform cost search down 
            # because i will be adding extra step of calculation.

            queue = sorted(queue, key=lambda x: len(x[1]))

            for child, move in self.getChildNodes(self.strToList(currentNode)):
                move = path + str(move)

                if child not in visited:
                    visited.append(child)
                    queue.append((child, move))
                    if child == "012345678":
                        return move
        return ""


    def dfs(self, maxDepth=35): # Depth first search
        visited = [self.listToStr(self.board)]
        vertex, path =  self.listToStr(self.board), ""
        stack = [(vertex, path)]

        if vertex == "012345678":
                return path

        while stack:
            vertex, path = stack.pop()

            self.visitedNodes = len(visited)
            self.activeNodes = len(stack)

            for child, move in self.getChildNodes(self.strToList(vertex)):
                move = path + str(move)
                if len(move) > maxDepth:
                    continue
                
                if child not in visited:
                    stack.append((child, move))
                    visited.append(child)
                    if child == "012345678":
                        return move
        return ""
    
    def ids(self): # Iterative deepening search
        max_depth = 35

        for i in range(1, max_depth):
            self.idsDepth = i
            if solution:=self.dfs(maxDepth=i): # 
                return solution
        return ""

    def evaluate(self, board: str):
        evaluation = 0
        for i in range(9):
            index =  board.index(str(i))
            y1, x1 = divmod(index, 3)
            y2, x2 = divmod(i, 3)
            evaluation += (abs(x1-x2)**2 + abs(y1-y2)**2) ** (1/2)
        return evaluation

    def gbs(self): # Greedy Best Search
        strBoard = self.listToStr(self.board)
        
        visited = [strBoard]
        queue = [(strBoard, "", self.evaluate(strBoard))]
        currentNode, path, h = queue[0]
        if currentNode == "012345678":
                return path

        while queue:
            queue = sorted(queue, key=lambda x: x[2]) # length of the path + evaluation value
            currentNode, path, value = queue.pop(0)

            self.visitedNodes = len(visited) # to show these stats in the tkinter
            self.activeNodes = len(queue)

         

            for child, move in self.getChildNodes(self.strToList(currentNode)):
                
                move = path + str(move)

                if child not in visited:
                    visited.append(child)
                    queue.append((child, move, self.evaluate(child)))
                    if child == "012345678":
                        return move
        return ""


    def aStar (self): # A* 
        strBoard = self.listToStr(self.board)
        
        visited = [strBoard]
        queue = [(strBoard, "", self.evaluate(strBoard))]
        currentNode, path, h = queue[0]
        if currentNode == "012345678":
                return path

        while queue:
            queue = sorted(queue, key=lambda x: len(x[1])+ x[2]) # length of the path + evaluation value
            currentNode, path, value = queue.pop(0)

            self.visitedNodes = len(visited) # to show these stats in the tkinter
            self.activeNodes = len(queue)

         

            for child, move in self.getChildNodes(self.strToList(currentNode)):
                
                move = path + str(move)

                if child not in visited:
                    visited.append(child)
                    queue.append((child, move, self.evaluate(child)))
                    if child == "012345678":

                        return move
        return ""

    def swapTiles(self, index, board):
        board = board.copy()
        index2 = board.index(8)
        board[index], board[index2] = board[index2], board[index]
        return board

    def allPossibleMoves(self, board):
        possibleMoves = []
        i = board.index(8) # index of empty tile
        row, column = divmod(i, 3) # get the row and column of empty tile

        if row == 0:
            possibleMoves.append(i+3)
        elif row == 1:
            possibleMoves.extend([i+3, i-3]) # add multiple elements to a list at the same time
        else: # row == 2
            possibleMoves.append(i-3)
        

        if column == 0:
            possibleMoves.append(i+1)
        elif column == 1:
            possibleMoves.extend([i+1, i-1])
        else: # column == 2
            possibleMoves.append(i-1)

        return possibleMoves


class GameWindow(tkinter.Tk):
    def __init__(self):
        super().__init__() # Run regular window initiation codes

        self.resizable(False, False) # make window unresizable
        self.title("Test search algorithms on 8 game") 
        
        self.gameFrame = tkinter.Frame(self)  # create a frame to put game in it
        self.gameFrame.grid(row=0, column=0, padx=30, pady=30) # place the frame into the window
    
        self.board = [i for i in range(9)]
        self.tileImages = {str(i): self.tileImage(i+1) for i in self.board}

        self.tiles = []

        for i in range(9):
            y, x = divmod(i, 3)
            self.tiles.append(tkinter.Button(
                self.gameFrame,
                image=self.tileImages[str(i)],
                command=partial(self.tileButtonFunc, i)
            ))
            self.tiles[i].grid(row=y, column=x, sticky="NWSE")
            
        
        
        self.bottomFrame = tkinter.Frame(self)
        self.bottomFrame.grid(row=1, column=0)
        
        self.shuffleButton = tkinter.Button(self.bottomFrame, text="Press to \nshuffle board", command=self.shuffleButtonFunc)
        self.shuffleButton.grid(row=0, column=0, rowspan=55, sticky="nes", padx=50, pady=20)
        
        self.vertexCounter = False


        self.rightBar = tkinter.Frame(self)
        self.rightBar.grid(row=0, column=1, padx=30)

        self.visitedVertexCounter = tkinter.Label(self.bottomFrame, text="Visited vertex number: 0")
        self.visitedVertexCounter.grid(row=0, column=1)

        self.activeVertexCounter = tkinter.Label(self.bottomFrame, text="Active vertex number: 0")
        self.activeVertexCounter.grid(row=1, column=1)

        self.timeLabel = tkinter.Label(self.bottomFrame, text="Calculation time: 0sn")
        self.timeLabel.grid(row=2, column=1)

        self.solutionLength =tkinter.Label(self.bottomFrame, text="Solution Length: 0")
        self.solutionLength.grid(row=3, column=1)

        self.idsDepthLabel = tkinter.Label(self.bottomFrame, text = "IDS Depth: 0")
        self.idsDepthLabel.grid(row=4, column=1)

        # ------------------------- BFS ------------------------------

        self.bfsLabel = tkinter.Label(self.rightBar, text="Breadth-first Search")
        self.bfsLabel.grid(row=0, column=0)

        self.bfsButton = tkinter.Button(self.rightBar, text="Solve", command=partial(self.solveFunc, "BFS"))
        self.bfsButton.grid(row=0, column=1, pady=10)

        # ------------------------- UCS ------------------------------

        self.ucsLabel = tkinter.Label(self.rightBar, text="Uniform- cost search")
        self.ucsLabel.grid(row=1, column=0)

        self.ucsButton = tkinter.Button(self.rightBar, text="Solve", command=partial(self.solveFunc, "UCS"))
        self.ucsButton.grid(row=1, column=1, pady=10)

        # -------------------------- DFS --------------------------------

        self.dfsLabel = tkinter.Label(self.rightBar, text="Depth first search")
        self.dfsLabel.grid(row=2, column=0)
        
        self.dfsButton = tkinter.Button(self.rightBar, text="Solve", command=partial(self.solveFunc, "DFS"))
        self.dfsButton.grid(row=2, column=1, pady=10)

        # ------------------------- IDS -----------------------------------

        self.idsLabel = tkinter.Label(self.rightBar, text="Iterative Deepening search")
        self.idsLabel.grid(row=3, column=0)

        self.idsButton = tkinter.Button(self.rightBar, text="Solve", command=partial(self.solveFunc, "IDS"))
        self.idsButton.grid(row=3, column=1, pady=10, padx=5)

        # ------------------------- GBS ------------------------------------

        self.gbsLabel = tkinter.Label(self.rightBar, text="Greedy Best search")
        self.gbsLabel.grid(row=4, column=0)

        self.gbsButton = tkinter.Button(self.rightBar, text="Solve", command=partial(self.solveFunc, "GBS"))
        self.gbsButton.grid(row=4, column=1, pady=10)

        # ------------------------- A* --------------------------------------

        self.aStarLabel = tkinter.Label(self.rightBar, text="A* search")
        self.aStarLabel.grid(row=5, column=0)

        self.aStarButton = tkinter.Button(self.rightBar, text="Solve", command=partial(self.solveFunc, "aStar"))
        self.aStarButton.grid(row=5, column=1, pady=10)
        
        # credits
        self.osmanLabel = tkinter.Label(self, text="Made by Osman Faruk Bayram \n 2003818")
        self.osmanLabel.grid(row=1, column=1)


        self.graph = Graph(self.board)
        self.calculationStartTime = time.time()
        self.updateSpecsClock()



  
    def allButtonsState(self, state):
        for tile in self.tiles:
            tile["state"] = state 

        self.shuffleButton["state"] = state
        self.bfsButton["state"] = state
        self.ucsButton["state"] = state
        self.dfsButton["state"] = state
        self.idsButton["state"] = state
        self.gbsButton["state"] = state
        self.aStarButton["state"] = state



    def updateSpecsClock(self):
        if self.vertexCounter:
            
            self.visitedVertexCounter["text"] = f"Visited vertex number: {self.graph.visitedNodes}"
            self.activeVertexCounter["text"] = f"Active vertex number: {self.graph.activeNodes}"
        
            difference = time.time() - self.calculationStartTime
            minutes, seconds = divmod(difference, 60)
            seconds = round(seconds, 2)

            self.timeLabel["text"] = f"Calculation time: {int(minutes)}min {seconds}sec"
            self.idsDepthLabel["text"] = f"IDS Depth: {self.graph.idsDepth}"
            self.visitedVertexCounter["text"] = f"Visited vertex number: {self.graph.visitedNodes}"
        self.after(100, self.updateSpecsClock)


    def solveFunc(self, n): 
        
        searchFunctions = {
            "BFS": (self.graph.bfs, self.bfsButton),
            "UCS": (self.graph.ucs, self.ucsButton),
            "DFS": (self.graph.dfs, self.dfsButton),
            "IDS": (self.graph.ids, self.idsButton),
            "GBS": (self.graph.gbs, self.gbsButton),
            "aStar": (self.graph.aStar, self.aStarButton)
        }
        
        thread = threading.Thread(target=partial(self.threadFunc, searchFunctions[n]))
        thread.start()
        

    def threadFunc(self, searchFunc):
        if self.graph.board == [i for i in range(9)]:
            return
        self.vertexCounter = True
        
        self.allButtonsState("disabled")
        searchFunc[1].configure(background="blue")

        self.calculationStartTime = time.time()
        solution = searchFunc[0]() # Action
        
        self.vertexCounter = False
        if solution:
            searchFunc[1].configure(background="green")
            moves = [int(move) for move in solution]
            self.solutionLength.configure(text=f"Solution Length: {len(solution)}")
            for move in moves:
                self.tileButtonFunc(move)
                time.sleep(moveDelay)
        else:
            searchFunc[1].configure(background="red")
        

        self.allButtonsState("normal")


    def tileButtonFunc(self, i):
        if i not in self.graph.allPossibleMoves(self.graph.board) or i == self.graph.board.index(8):
            return

        self.graph.board = self.graph.swapTiles(i, self.graph.board)
        self.updateTiles()
        
    def isBoardValid(self, array):
        inverseCount = 0
        emptyValue = 8
        for i in range(9):
            for j in range(i + 1, 9):
                if array[j] != emptyValue and array[i] != emptyValue and array[i] > array[j]:
                    inverseCount += 1
        return inverseCount % 2 == 0

    def shuffleButtonFunc(self):
        random.shuffle(self.graph.board)
        while not self.isBoardValid(self.graph.board):
            random.shuffle(self.graph.board)
            
        self.updateTiles()


    def updateTiles(self):
        for i in range(9):
            value = self.graph.board[i]
            self.tiles[i].config(image=self.tileImages[str(value)])


    def tileImage(self, input):
        if input == 9:
            input = " "
        width, height = 150, 150
        tileBackgroundColor = (240, 240, 240)
        textColor = (20, 25, 40)
        image = Image.new("RGB", (width, height), color=tileBackgroundColor)
        font = ImageFont.truetype("OpenSans.ttf", size=90)
        drawer = ImageDraw.Draw(image)
        drawer.text((width/2, height/2), str(input), font=font, fill=textColor, anchor="mm")
        return ImageTk.PhotoImage(image)



if __name__ == "__main__":
    game = GameWindow()
    game.mainloop() # start game

