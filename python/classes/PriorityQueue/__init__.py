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
            if prior is None or prior < value:
                item = key
                prior = value
        self.__queue.pop(item)
        return item, prior
