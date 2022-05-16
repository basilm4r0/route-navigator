import xlrd
from queue import PriorityQueue

class State(object):

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

    def GetDistance(self):
        pass

    def CreateChildren(self):
        pass

class State_String(State):
    def __init__(self,name,parent,
                 start = 0,
                 goal = 0):

        super(State_String, self).__init__(name, parent, start, goal)
        self.aerialdist = self.GetAerialDistance()
        self.walkindist = self.GetWalkingDistance()

    def GetAerialDistance(self):

        if self.name == self.goal:
            return 0
        o = SearchList(aerial_list, self.name)
        i = SearchList(aerial_list, self.goal)
        aerialdist = sheet.cell_value(o,i)
        return aerialdist

    def GetWalkingDistance(self):

        if self.name == self.goal:
            return 0
        o = SearchList(walking_list, self.name)
        i = SearchList(walking_list, self.goal)
        walkingdist = sheet.cell_value(o,i)
        return walkingdist

    def CreateChildren(self):
        if not self.children:
            o = SearchSheet(driving_sheet, self.name)
            for i in range(driving_sheet.ncols):
                
                if (str(driving_sheet.cell_value(o,i)) != ""):
                    name = driving_shee.cell_value(0,i)
                child = State_String(name, self)
                self.children.append(child)

class AStar_Solver:
    def __init__(self, start , goal):
        self.path          = []
        self.visitedQueue  = []
        self.priorityQueue = PriorityQueue()
        self.start         = start
        self.goal          = goal

    def Solve(self):
        startState = State_String(self.start,
                                  0,
                                  self.start,
                                  self.goal)

        count = 0
        self.priorityQueue.put((0,count,startState))

        while(not self.path and self.priorityQueue.qsize()):
            closestChild = self.priorityQueue.get()[2]
            closestChild.CreateChildren()
            self.visitedQueue.append(closestChild.name)

            for child in closestChild.children:
                if child.name not in self.visitedQueue:
                    count +=1
                    if not child.dist:
                        self.path = child.path
                        break
                    self.priorityQueue.put((child.dist,count,child))

        if not self.path:
            print("Goal of %s is not possible!" % (self.goal))

        return self.path

def SearchSheet(sheet, name):
    for o in range(sheet.rows):
        if (sheet.cell_value(o,0) == name):
            return o

if __name__ == "__main__":
    location = ("./DB_Cities.xls")
    workbook = xlrd.open_workbook(location)
    aerial_sheet = workbook.sheet_by_index(0)
    walking_sheet = workbook.sheet_by_index(1)
    driving_sheet = workbook.sheet_by_index(2)

    start1 = "Dura"
    goal1  = "Safad"
    print("Starting...")

    a = AStar_Solver(start1, goal1)
    a.Solve()

    for i in range(len(a.path)):
        print("{0}) {1}".format(i, a.path[i]))
