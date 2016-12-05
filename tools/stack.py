class stack():
    def __init__(self):
        self.item = []

    def is_Empty(self):
        return self.item == []

    def push(self, item):
        self.item.append(item)

    def pop(self):
        return self.item.pop()

    def size(self):
        return len(self.item)

    def top(self):
        return self.item[len(self.item) - 1]

    def get_item(self):
        return self.item
