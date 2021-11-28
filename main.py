from functools import partial
import tkinter
from collections import defaultdict
from PIL import Image, ImageDraw, ImageTk, ImageFont
import random
import time
import numpy as np
import threading
import sys
random.seed(42)# i need to test the algorithms on the same boards to check if they work consistently

# i have used the walrus operator in this script so your python version must be higher from 3.8
assert sys.version_info > (3, 8), "Use Python 3.8 or newer"

# https://www.baeldung.com/cs/iterative-deepening-vs-depth-first-search

moveDelay = 0.3   # s
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
      
    def bfs(self):     
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
                print(child, move, len(move), "queue length: ", len(queue))

                if child not in visited:
                    visited.append(child)
                    queue.append((child, move))
                    if child == "012345678":
                        return move

        print("This is a complete search. This is not supposed to happen!!")

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
                print(child, move, len(move), "queue length: ", len(queue))

                if child not in visited:
                    visited.append(child)
                    queue.append((child, move))
                    if child == "012345678":
                        return move

    def dfs(self, maxDepth=40): # Depth first search
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
                print(child, move, "\t", len(move), "queue length: ", len(stack))
                if child not in visited:
                    stack.append((child, move))
                    visited.append(vertex)
                    if vertex == "012345678":
                        return path
        return ""
    
    def ids(self): # Iterative deepening search
        max_depth = 35

        for i in range(1, max_depth):
            self.idsDepth = i
            if solution:=self.dfs(i, maxDepth=i): # 
                return solution



    def gbs(self): # Greedy Best Search
        ...

    def aStar(self): # A*
        ...
    
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
        self.gameFrame.grid(row=0, column=0) # place the frame into the window
    
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
        
        self.shuffleButton = tkinter.Button(self.bottomFrame, text="Press to shuffle board", command=self.shuffleButtonFunc)
        self.shuffleButton.grid(row=0, column=0)
        
        self.vertexCounter = False


        self.rightBar = tkinter.Frame(self)
        self.rightBar.grid(row=0, column=1)

        self.visitedVertexCounter = tkinter.Label(self.bottomFrame, text="Visited vertex number: 0")
        self.visitedVertexCounter.grid(row=0, column=1)

        self.activeVertexCounter = tkinter.Label(self.bottomFrame, text="Active vertex number: 0")
        self.activeVertexCounter.grid(row=1, column=1)

        self.timeLabel = tkinter.Label(self.bottomFrame, text="Calculation time: 0sn")
        self.timeLabel.grid(row=2, column=1)

        # ------------------------- BFS ------------------------------


        

        self.bfsLabel = tkinter.Label(self.rightBar, text="Breadth-first Search")
        self.bfsLabel.grid(row=0, column=0)

        
        
        self.bfsCalculateButton = tkinter.Button(self.rightBar, text="Solve", command=partial(self.solveFunc, "BFS"))
        self.bfsCalculateButton.grid(row=0, column=1)

        

        # ------------------------- UCS ------------------------------

      

        self.ucsLabel = tkinter.Label(self.rightBar, text="Uniform- cost search")
        self.ucsLabel.grid(row=1, column=0)

        

        self.ucsStartButton = tkinter.Button(self.rightBar, text="Solve", command=partial(self.solveFunc, "UCS"))
        self.ucsStartButton.grid(row=1, column=1)


        # -------------------------- DFS --------------------------------

        self.dfsLabel = tkinter.Label(self.rightBar, text="Depth first search")
        self.dfsLabel.grid(row=2, column=0)
        
        self.dfsCalculateButton = tkinter.Button(self.rightBar, text="Solve", command=partial(self.solveFunc, "DFS"))
        self.dfsCalculateButton.grid(row=2, column=1)

        self.graph = Graph(self.board)
        self.updateSpecsClock()

  
    def allButtonsState(self, state):
        for tile in self.tiles:
            tile["state"] = state 

        #self.shuffleButton["state"] = state
        #self.bfsCalculateButton["state"] = state
        #self.ucsCalculateButton["state"] = state


    def updateSpecsClock(self):
        if self.vertexCounter:
            self.visitedVertexCounter["text"] = f"Visited vertex number: {self.graph.visitedNodes}"
            self.activeVertexCounter["text"] = f"Active vertex number: {self.graph.activeNodes}"
        

        self.visitedVertexCounter["text"] = f"Visited vertex number: {self.graph.visitedNodes}"
        self.after(100, self.updateSpecsClock)


    def solveFunc(self, n): 
        
        searchFunctions = {
            "BFS": self.graph.bfs,
            "UCS": self.graph.ucs,
            "DFS": self.graph.dfs,
        }
        
        thread = threading.Thread(target=partial(self.threadFunc, searchFunctions[n]))
        thread.start()
        

    def threadFunc(self, func):
        self.vertexCounter = True
        self.allButtonsState("disabled")


        startTime = time.time()
        solution = func() # Action
        difference = time.time() - startTime
        minutes, seconds = divmod(difference, 60)
        seconds = round(seconds, 2)


        self.timeLabel["text"] = f"Calculation time: {int(minutes)}min {seconds}sec"
        
        self.vertexCounter = False
        print("solution: ",solution)
        moves = [int(move) for move in solution]

        for move in moves:
            self.tileButtonFunc(move)
            time.sleep(moveDelay)

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
        print("shuffled Once")
        while not self.isBoardValid(self.graph.board):
            random.shuffle(self.graph.board)
            print("shuffled twice")
       # print(self.isBoardValid([7,5,2,0,6,8,3,4,1]), "if this false, You stupid ass")
        #print(self.isBoardValid(self.graph.board), "if this false, You stupid ass")
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

