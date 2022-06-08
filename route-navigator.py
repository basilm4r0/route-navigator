import xlrd     #library for reading .xls files
from queue import PriorityQueue

class Node(object):     #parent class for node object
    def __init__(self, name, parent,
                 start = 0,
                 goal = 0):

        self.children = []
        self.parent = parent
        self.name = name
        self.cost = 0
        self.aerialdist = 0
        self.walkingdist = 0

        if parent:
            self.start  = parent.start
            self.goal   = parent.goal
            self.path   = parent.path[:]
            self.path.append(name)
        else:
            self.path   = [name]
            self.start  = start
            self.goal   = goal

    def GetAerialDistance(self):
        pass

    def GetWalkingDistance(self):
        pass

    def CreateChildren(self):
        pass

class City_Node(Node):      #child class for city nodes
    def __init__(self,name,parent,cost,     #city node object constructor
                 start = 0,
                 goal = 0):

        super(City_Node, self).__init__(name, parent, start, goal)
        if parent:
            self.cost = float(parent.cost) + float(cost)
        else:
            self.cost = cost
        self.aerialdist = self.GetAerialDistance()
        self.walkingdist = self.GetWalkingDistance()

    def GetAerialDistance(self):        #retrieves aerial distance from spreadsheet

        if self.name == self.goal:
            return 0
        o = SearchSheet(aerial_sheet, self.name)
        i = SearchSheet(aerial_sheet, self.goal)
        aerialdist = float(aerial_sheet.cell_value(o,i))
        return aerialdist

    def GetWalkingDistance(self):       #retrieves walking distance from spreadsheet

        if self.name == self.goal:
            return 0
        o = SearchSheet(walking_sheet, self.name)
        i = SearchSheet(walking_sheet, self.goal)
        walkingdist = float(walking_sheet.cell_value(o,i))
        return walkingdist

    def CreateChildren(self):           #expands city node (creates children)
        if not self.children:
            o = SearchSheet(driving_sheet, self.name)
            for i in range(1, driving_sheet.ncols):
                if (str(driving_sheet.cell_value(o,i)) != ""):
                    name = driving_sheet.cell_value(0,i)
                    child = City_Node(name, self, float(driving_sheet.cell_value(o,i)))
                    self.children.append(child)

class AStar_Solver:         #A* algorithm solver class
    def __init__(self, start , goal, heuristic):
        self.path          = []
        self.visitedQueue  = []
        self.priorityQueue = PriorityQueue()
        self.start         = start
        self.goal          = goal
        self.heuristic    = heuristic
        self.cost          = 0

    def Solve(self):        #Solving algorithm method
        startState = City_Node(self.start, 0, 0,
                                  self.start,
                                  self.goal)

        count = 0
        if self.heuristic == 1:
            self.priorityQueue.put((startState.cost + startState.aerialdist, count, startState))#priority = cumelative cost + heuristic
        elif self.heuristic == 2:
            self.priorityQueue.put((startState.cost + startState.walkingdist, count, startState))
        while(self.priorityQueue.qsize()):
            closestChild = self.priorityQueue.get()[2]
            self.visitedQueue.append(closestChild.name)
            if (closestChild.name == self.goal):
                self.path = closestChild.path
                self.cost = closestChild.cost
                break
            closestChild.CreateChildren()
            for child in closestChild.children:
                count += 1
                if self.heuristic == 1:
                    self.priorityQueue.put((child.cost + child.aerialdist, count, child))
                elif self.heuristic == 2:
                    self.priorityQueue.put((child.cost + child.walkingdist, count, child))

        if not self.path:
            print("Goal of %s is not possible!" % (self.goal))

        return self.path

class Greedy_Solver:        #Greedy search pathfinding algorithm class
    def __init__(self, start , goal, heuristic):
        self.path          = []
        self.visitedQueue  = []
        self.priorityQueue = PriorityQueue()
        self.start         = start
        self.goal          = goal
        self.heuristic    = heuristic
        self.cost          = 0

    def Solve(self):        #algorithm solving method
        startState = City_Node(self.start, 0, 0,
                                  self.start,
                                  self.goal)

        count = 0
        if self.heuristic == 1:
            self.priorityQueue.put((startState.aerialdist, count, startState)) #priority = hearistic
        elif self.heuristic == 2:
            self.priorityQueue.put((startState.walkingdist, count, startState))
        while(not self.path and self.priorityQueue.qsize()):
            closestChild = self.priorityQueue.get()[2]
            self.visitedQueue.append(closestChild.name)
            if (closestChild.name == self.goal):
                self.path = closestChild.path
                self.cost = closestChild.cost
                break
            closestChild.CreateChildren()
            for child in closestChild.children:
                count += 1
                if self.heuristic == 1:
                    self.priorityQueue.put((child.aerialdist, count, child))
                elif self.heuristic == 2:
                    self.priorityQueue.put((child.walkingdist, count, child))

        if not self.path:
            print("Goal of %s is not possible!" % (self.goal))

class BFS_Solver:       # Breadth-first search algorith class
    def __init__(self, start , goal):
        self.path          = []
        self.visitedQueue  = []
        self.priorityQueue = PriorityQueue()
        self.start         = start
        self.goal          = goal
        self.cost          = 0

    def Solve(self):    # algorithm solving method
        startState = City_Node(self.start, 0, 0,
                                  self.start,
                                  self.goal)

        count = 0
        self.priorityQueue.put((count, startState))     #priority = node number
        while(not self.path and self.priorityQueue.qsize()):
            closestChild = self.priorityQueue.get()[1]
            self.visitedQueue.append(closestChild.name)
            if (closestChild.name == self.goal):
                self.path = closestChild.path
                self.cost = closestChild.cost
                break
            closestChild.CreateChildren()
            for child in closestChild.children:
                count += 1
                self.priorityQueue.put((count, child))

        if not self.path:
            print("Goal of %s is not possible!" % (self.goal))

def SearchSheet(sheet, name):   # Searches first column of input spreadsheet for input string. returns row number
    for o in range(sheet.nrows):
        if (sheet.cell_value(o,0) == name):
            return o

if __name__ == "__main__":      # Main body of program
    try:
        location = ("./DB_Cities.xls")      # defining spreadsheet path and opening sheets
        workbook = xlrd.open_workbook(location)
        aerial_sheet = workbook.sheet_by_index(0)
        walking_sheet = workbook.sheet_by_index(1)
        driving_sheet = workbook.sheet_by_index(2)


        start1 = input("Enter the city that is the starting point: ")
        if (SearchSheet(driving_sheet, start1) == None):
            print("Starting point input invalid.")
            quit()

        goal1  = input("Enter the city that is the ending point: ")
        if (SearchSheet(driving_sheet, goal1) == None):
            print("Destination point input invalid.")
            quit()

        method = input("Enter 1 to use A*, 2 to use greedy search, 3 to use breadth-first search: ")
        if int(method) == 1:
            heuristic = input("Enter 1 to use aerial distance as a heuristic or 2 to use walking distance as a heuristic: ")
            if (int(heuristic) != 1 and int(heuristic) != 2):
                print("Heuristic input invalid.")
                quit()
            a = AStar_Solver(start1, goal1, int(heuristic))

        elif int(method) == 2:
            heuristic = input("Enter 1 to use aerial distance as a heuristic or 2 to use walking distance as a heuristic: ")
            if (int(heuristic) != 1 and int(heuristic) != 2):
                print("Heuristic input invalid.")
                quit()
            a = Greedy_Solver(start1, goal1, int(heuristic))

        elif int(method) == 3:
            a = BFS_Solver(start1, goal1)

        else:
            print("Method input invalid.")
            quit()
        print("\nStarting...\n")
        a.Solve()

        print("Solution:")      #printing solution found by algorithm
        for i in range(len(a.path)):
            print("\t{0}) {1}".format(i, a.path[i]))
        print("\nPath cost: %s" % a.cost)
        print("\nVisited Nodes:")       #printing nodes visited by algorithm
        for i in range(len(a.visitedQueue)):
            print("\t{0}) {1}".format(i, a.visitedQueue[i]))
    except KeyboardInterrupt:
        print(" Pressed, exiting program...")   #exit program peacefully in case of user keyboard interrupt
        quit()
