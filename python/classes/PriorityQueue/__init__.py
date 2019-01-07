import heapq


class PriorityQueueByDict:

    def __init__(self):
        self.__queue = dict()

    def empty(self):
        return len(self.__queue.keys()) == 0

    def update(self, item, priority=0):
        self.__queue.update({item: priority})

    def get(self):
        item = None
        prior = None
        for key, value in self.__queue.items():
            if prior is None:
                item = key
                prior = value
            elif prior > value:
                item = key
                prior = value

        self.__queue.pop(item)
        return item, prior


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def is_empty(self):
        return len(self.elements) == 0

    def push(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def pop(self):
        return heapq.heappop(self.elements)[1]
