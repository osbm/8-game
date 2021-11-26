from functools import partial
import tkinter
from collections import defaultdict
from PIL import Image, ImageDraw, ImageTk, ImageFont
import random
import time
import numpy as np
import threading

random.seed(42)
# Add as much as comment as possible
# TODO(osman) set fixed width to right panel
# TODO(osman) set a bell that rings after calculation is done.
# https://www.baeldung.com/cs/iterative-deepening-vs-depth-first-search

moveDelay = 0.3

class Graph:
    def __init__(self, board):
        self.board = board

        self.visitedNodes = 0
        

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

            #visited.append(currentNode)
            
            #if currentNode == "012345678":
            #    return path

            self.visitedNodes = len(visited)

            for child, move in self.getChildNodes(self.strToList(currentNode)):
                move = path + str(move)
                #print(child, move, len(move), "queue length: ", len(queue))

                if child not in visited:
                    visited.append(child)
                    queue.append((child, move))
                    if child == "012345678":
                        return move

        print("This is not supposed to happen!!")
   
    def ucs(self): # Uniform- cost search
        # https://www.geeksforgeeks.org/uniform-cost-search-dijkstra-for-large-graphs/
        visited = []
        queue = [[self.listToStr(self.board), ""]]
        
        while queue:
            currentNode, path = queue.pop(0)
            visited.append(currentNode)
            
            if currentNode == "012345678":
                return path

            self.visitedNodes = len(visited)
            


            for child, move in self.getChildNodes(self.strToList(currentNode)):
                move = path + str(move)
                if child not in visited:
                    visited.append(child)
                    queue.append([child, move])
                    if child == "012345678":
                        return move

        print("This is not supposed to happen!!")

    def dfs(self): # Depth first search
        visited = []
        vertex, path =  self.listToStr(self.board), ""
        stack = [(vertex, path)]

        while stack:
            vertex, path = stack.pop()
            self.visitedNodes = len(visited)
            if vertex == "012345678":
                return path
            
            if vertex not in visited:
                visited.append(vertex)

            for child, move in self.getChildNodes(self.strToList(vertex)):
                move = path + str(move)
                
                if child == "012345678":
                    return move

                if len(move) > 40:
                    continue

                if child not in visited:
                    stack.append((child, move))
        print("THIS IS NOT POSSIBLE")
    
    # Iterative deepening search
    # greedy best search
    # a* search

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
        # TODO(osman) add fonts to the button labels.
        self.shuffleButton = tkinter.Button(self.bottomFrame, text="Press to shuffle board", command=self.shuffleButtonFunc)
        self.shuffleButton.grid(row=0, column=0)
        
        self.vertexCounter = False


        self.rightBar = tkinter.Frame(self)
        self.rightBar.grid(row=0, column=1)

        self.visitedVertexCounter = tkinter.Label(self.bottomFrame, text="Visited vertex number: 0")
        self.visitedVertexCounter.grid(row=0, column=1)

        self.timeLabel = tkinter.Label(self.bottomFrame, text="Calculation time: 0sn")
        self.timeLabel.grid(row=1, column=1)

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
        self.vertexLabelUpdateClock()

  
    def allButtonsState(self, state):
        for tile in self.tiles:
            tile["state"] = state 

        #self.shuffleButton["state"] = state
        #self.bfsCalculateButton["state"] = state
        #self.ucsCalculateButton["state"] = state


    def vertexLabelUpdateClock(self):
        if self.vertexCounter:
            self.visitedVertexCounter["text"] = f"Visited vertex number: {self.graph.visitedNodes}"

        self.visitedVertexCounter["text"] = f"Visited vertex number: {self.graph.visitedNodes}"
        self.after(1000, self.vertexLabelUpdateClock)


    def solveFunc(self, n): 
        
        searchFunctions = {
            "BFS": self.graph.bfs,
            "DFS": self.graph.dfs,
            "UCS": self.graph.ucs
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


        self.timeLabel["text"] = f"Calculation time: {minutes}min {seconds}sec"
        
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
        
        
    def shuffleButtonFunc(self):
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

