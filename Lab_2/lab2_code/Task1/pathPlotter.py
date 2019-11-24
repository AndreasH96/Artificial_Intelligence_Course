
import random
import numpy as np
import matplotlib.pyplot as plt
import time
class ScatterPlotter:
    def __init__(self):
        super().__init__()
        self.path = []
        #self.map
    
        #plt.show()
    def plot(self,map2d, path,title):
        import matplotlib.cm as cm
        plt.clf()
        plt.interactive(False)

        greennumber = map2d.max()
        #greennumber = len(np.unique(map2d_))
        #print(greennumber)
        colors = cm.winter(np.linspace(0, 1, greennumber))

        colorsMap2d = [[[] for x in range(map2d.shape[1])] for y in range(map2d.shape[0])]
        # Assign RGB Val for starting point and ending point
        locStart, locEnd = np.where(map2d == -2), np.where(map2d == -3)

        colorsMap2d[locStart[0][0]][locStart[1][0]] = [.0, 1.0, .0, 1.0]  # black
        colorsMap2d[locEnd[0][0]][locEnd[1][0]] = [.0, .0, 1.0, 1.0]  # white

        # Assign RGB Val for obstacle
        locObstacle = np.where(map2d == -1)
        for iposObstacle in range(len(locObstacle[0])):
            colorsMap2d[locObstacle[0][iposObstacle]][locObstacle[1][iposObstacle]] = [1.0, .0, .0, 1.0]
        # Assign 0
        locZero = np.where(map2d == 0)
        
        for iposZero in range(len(locZero[0])):
            colorsMap2d[locZero[0][iposZero]][locZero[1][iposZero]] = [1.0, 1.0, 1.0, 1.0]
        
        
        # Assign Expanded nodes
        locExpand = np.where(map2d>0)
        #print(locExpand)
        #print(colorsMap2d)
        for iposExpand in range(len(locExpand[0])):
            #print(locExpand[1][iposExpand])
            colorsMap2d[locExpand[1][iposExpand]][locExpand[0][iposExpand]] = [.0, .0, .0, 1.0]##colors[map2d[locExpand[0][iposExpand]][locExpand[1][iposExpand]]-1]

        for irow in range(len(colorsMap2d)):
            for icol in range(len(colorsMap2d[irow])):
                if colorsMap2d[irow][icol] == []:
                    colorsMap2d[irow][icol] = [1.0, 0.0, 0.0, 1.0]

        plt.scatter(x = map2d[0], y = map2d[1])
        plt.title(title)
        plt.imshow(colorsMap2d, interpolation='nearest')
        #plt.colorbar()
        plt.plot(path[:][0],path[:][1], color='magenta',linewidth=2.5)
        plt.ylim(0,map2d.shape[0])
        plt.xlim(0,map2d.shape[1])
        plt.draw
        plt.pause(1e-17)
        time.sleep(0.001)
        #plt.savefig("Test.png")
        plt.show()
    def scatterPlot(self,map2d, path, title =" "):
        import matplotlib.cm as cm
        plt.interactive(False)

        greennumber = map2d.max()
        #greennumber = len(np.unique(map2d_))
        #print(greennumber)
        colors = cm.winter(np.linspace(0, 1, greennumber))

        colorsMap2d = [[[] for x in range(map2d.shape[1])] for y in range(map2d.shape[0])]
        # Assign RGB Val for starting point and ending point
        locStart, locEnd = np.where(map2d == -2), np.where(map2d == -3)

        colorsMap2d[locStart[0][0]][locStart[1][0]] = [.0, .0, .0, 1.0]  # black
        colorsMap2d[locEnd[0][0]][locEnd[1][0]] = [.0, .0, 1.0, 1.0]  # white

        # Assign RGB Val for obstacle
        locObstacle = np.where(map2d == -1)
        for iposObstacle in range(len(locObstacle[0])):
            colorsMap2d[locObstacle[0][iposObstacle]][locObstacle[1][iposObstacle]] = [1.0, .0, .0, 1.0]
        # Assign 0
        locZero = np.where(map2d == 0)

        for iposZero in range(len(locZero[0])):
            colorsMap2d[locZero[0][iposZero]][locZero[1][iposZero]] = [1.0, 1.0, 1.0, 1.0]

        # Assign Expanded nodes
        locExpand = np.where(map2d>0)

        for iposExpand in range(len(locExpand[0])):
            colorsMap2d[locExpand[0][iposExpand]][locExpand[1][iposExpand]] = colors[map2d[locExpand[0][iposExpand]][locExpand[1][iposExpand]]-1]

        for irow in range(len(colorsMap2d)):
            for icol in range(len(colorsMap2d[irow])):
                if colorsMap2d[irow][icol] == []:
                    colorsMap2d[irow][icol] = [1.0, 0.0, 0.0, 1.0]

        plt.scatter(x = map2d[0], y = map2d[1])
        plt.title(title)
        plt.imshow(colorsMap2d, interpolation='nearest')
        plt.colorbar()
        #plt.plot(path[:][0],path[:][1], color='magenta',linewidth=2.5)
        plt.ylim(0,map2d.shape[0])
        plt.xlim(0,map2d.shape[1])
        plt.draw()
        #plt.savefig()
        #plt.show()