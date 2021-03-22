import random

class Bag:
    """
    Bag class facilitates random sampling of items
    """
    def __init__(self):
        self.numItems = 20
        self.utility = [random.randint(1,100) for i in range(self.numItems)]

    def show_utility(self):
        return sorted(self.utility)

    def sample_item(self):
        return self.utility[random.randint(0,self.numItems-1)]


