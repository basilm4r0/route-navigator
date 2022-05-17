import xlrd
from queue import PriorityQueue

class Node(object):

    '''
    Steps:
    1) Generate a list of all possible next Steps toward goal from current position
    2) Store Children in PriorityQueue based on distance to goal, closest first
    3) Select closest child and Repeat until goal reached or no more Children
    '''

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

class City_Node(Node):
    def __init__(self,name,parent,cost,
                 start = 0,
                 goal = 0):

        super(City_Node, self).__init__(name, parent, start, goal)
        if parent:
            self.cost = int(parent.cost) + int(cost)
        else:
            self.cost = cost
        self.aerialdist = self.GetAerialDistance()
        self.walkingdist = self.GetWalkingDistance()

    def GetAerialDistance(self):

        if self.name == self.goal:
            return 0
        o = SearchSheet(aerial_sheet, self.name)
        i = SearchSheet(aerial_sheet, self.goal)
        aerialdist = int(aerial_sheet.cell_value(o,i))
        return aerialdist

    def GetWalkingDistance(self):

        if self.name == self.goal:
            return 0
        o = SearchSheet(walking_sheet, self.name)
        i = SearchSheet(walking_sheet, self.goal)
        walkingdist = int(walking_sheet.cell_value(o,i))
        print(o, i, walkingdist)
        return walkingdist

    def CreateChildren(self):
        if not self.children:
            o = SearchSheet(driving_sheet, self.name)
            for i in range(1, driving_sheet.ncols):
                
                if (str(driving_sheet.cell_value(o,i)) != ""):
                    name = driving_sheet.cell_value(0,i)
                    child = City_Node(name, self, int(driving_sheet.cell_value(o,i)))
                    self.children.append(child)

class AStar_Solver:
    def __init__(self, start , goal, heuristic):
        self.path          = []
        self.visitedQueue  = []
        self.priorityQueue = PriorityQueue()
        self.start         = start
        self.goal          = goal
        self.heuristic    = heuristic
        self.cost          = 0

    def Solve(self):
        startState = City_Node(self.start, 0, 0,
                                  self.start,
                                  self.goal)

        count = 0
        if self.heuristic == 1:
            self.priorityQueue.put((startState.cost + startState.aerialdist, count, startState))
        elif self.heuristic == 2:
            self.priorityQueue.put((startState.cost + startState.walkingdist, count, startState))
        while(self.priorityQueue.qsize()):
            closestChild = self.priorityQueue.get()[2]
            if closestChild.name in self.visitedQueue:
                continue
            self.visitedQueue.append(closestChild.name)
            if (closestChild.name == self.goal):
                self.path = closestChild.path
                self.cost = closestChild.cost
                break
            closestChild.CreateChildren()
            for child in closestChild.children:
                if child.name not in self.visitedQueue:
                    count += 1
                    if self.heuristic == 1:
                        self.priorityQueue.put((child.cost + child.aerialdist, count, child))
                    elif self.heuristic == 2:
                        self.priorityQueue.put((child.cost + child.walkingdist, count, child))
                    print(child.name, child.cost, child.walkingdist, child.cost+child.walkingdist)

        if not self.path:
            print("Goal of %s is not possible!" % (self.goal))

        return self.path

class Greedy_Solver:
    def __init__(self, start , goal, heuristic):
        self.path          = []
        self.visitedQueue  = []
        self.priorityQueue = PriorityQueue()
        self.start         = start
        self.goal          = goal
        self.heuristic    = heuristic
        self.cost          = 0

    def Solve(self):
        startState = City_Node(self.start, 0, 0,
                                  self.start,
                                  self.goal)

        count = 0
        if self.heuristic == 1:
            self.priorityQueue.put((startState.aerialdist, count, startState))
        elif self.heuristic == 2:
            self.priorityQueue.put((startState.walkingdist, count, startState))
        while(not self.path and self.priorityQueue.qsize()):
            closestChild = self.priorityQueue.get()[2]
            if closestChild.name in self.visitedQueue:
                continue
            self.visitedQueue.append(closestChild.name)
            if (closestChild.name == self.goal):
                self.path = closestChild.path
                self.cost = closestChild.cost
                break
            closestChild.CreateChildren()
            for child in closestChild.children:
                if child.name not in self.visitedQueue:
                    count += 1
                    if self.heuristic == 1:
                        self.priorityQueue.put((child.aerialdist, count, child))
                    elif self.heuristic == 2:
                        self.priorityQueue.put((child.walkingdist, count, child))

        if not self.path:
            print("Goal of %s is not possible!" % (self.goal))

class BFS_Solver:
    def __init__(self, start , goal, heuristic):
        self.path          = []
        self.visitedQueue  = []
        self.priorityQueue = PriorityQueue()
        self.start         = start
        self.goal          = goal
        self.heuristic    = heuristic
        self.cost          = 0

    def Solve(self):
        startState = City_Node(self.start, 0, 0,
                                  self.start,
                                  self.goal)

        count = 0
        if self.heuristic == 1:
            self.priorityQueue.put((count, startState))
        elif self.heuristic == 2:
            self.priorityQueue.put((count, startState))
        while(not self.path and self.priorityQueue.qsize()):
            closestChild = self.priorityQueue.get()[1]
            if closestChild.name in self.visitedQueue:
                continue
            self.visitedQueue.append(closestChild.name)
            if (closestChild.name == self.goal):
                self.path = closestChild.path
                self.cost = closestChild.cost
                break
            closestChild.CreateChildren()
            for child in closestChild.children:
                if child.name not in self.visitedQueue:
                    count += 1
                    if self.heuristic == 1:
                        self.priorityQueue.put((count, child))
                    elif self.heuristic == 2:
                        self.priorityQueue.put((count, child))

        if not self.path:
            print("Goal of %s is not possible!" % (self.goal))

def SearchSheet(sheet, name):
    for o in range(sheet.nrows):
        if (sheet.cell_value(o,0) == name):
            return o

if __name__ == "__main__":
    location = ("./DB_Cities.xls")
    workbook = xlrd.open_workbook(location)
    aerial_sheet = workbook.sheet_by_index(0)
    walking_sheet = workbook.sheet_by_index(1)
    driving_sheet = workbook.sheet_by_index(2)

    start1 = "Ramallah"
    goal1  = "Safad"
    print("Starting...")

    a = AStar_Solver(start1, goal1, 1)
    a.Solve()

    print("Solution:")
    for i in range(len(a.path)):
        print("\t{0}) {1}".format(i, a.path[i]))
    print("\nPath cost: %s" % a.cost)
    print("\nVisited Nodes:")
    for i in range(len(a.visitedQueue)):
        print("\t{0}) {1}".format(i, a.visitedQueue[i]))

