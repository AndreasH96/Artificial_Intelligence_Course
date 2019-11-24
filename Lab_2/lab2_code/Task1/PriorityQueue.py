import heapq

# Priority Queue based on heapq
class PriorityQueue:
    def __init__(self):
        self.elements = []
    def isEmpty(self):
        return len(self.elements) == 0
    ''' def add(self, item, priority):
        heapq.heappush(self.elements,(priority,item)) '''
    def add(self,item,priority):
        self.elements.append([priority,item])
    ''' def remove(self):
        #print(self.elements)
        return heapq.heappop(self.elements)[1] '''
    def removeLast(self):
        #print(self.elements)
        lastElement = self.elements[len(self.elements) -1]
        self.elements.remove(lastElement)
        #print(self.elements)
        return lastElement [1]
    def removeFirst(self):
        #print(self.elements)
        firstElement = self.elements[0]
        self.elements.remove(firstElement)
        #print(self.elements)
        return firstElement [1]
    def removeWithLeastCost(self):
        return heapq.heappop(self.elements)[1]