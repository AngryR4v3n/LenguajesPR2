class Stack:
    def __init__(self):
        self.array = []

    def is_empty(self):
        if len(self.array) == 0:
            return True
        else:
            return False

    def peek(self):
        return self.array[-1]

    def pop(self):
        if not self.is_empty():
            return self.array.pop()
        else: 
            return "-1"
    def add(self, elem):
        self.array.append(elem)

    def length(self):
        return len(self.array)

    def __repr__(self):
        return f'<Stack with {self.array}'