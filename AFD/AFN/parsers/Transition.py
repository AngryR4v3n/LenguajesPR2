class Transition: 
    def __init__(self, start=None, transition=None, end=None):
        self.start = start
        self.transition = transition
        self.end = end
        self.mark = False
        self.index = None
        self.isFinal = False
        self.isInitial = False

    def get_start(self):
        return self.start

    def set_start(self, data):
        self.start = data

    def get_transition(self):
        return self.transition
    
    def get_end(self):
        return self.end
    
    def set_end(self, data):
        self.end = data

    def set_initial(self, boolean):
        self.isInitial = boolean

    def set_final(self, boolean):
        self.isFinal = boolean
    
    def get_mark(self):
        return self.mark
    
    def set_mark(self, data):
        self.mark = data

    #used for name reassignment.
    def set_index(self, data):
        self.index = data

    def __repr__(self):
        return f'<Transition from: {self.start} to {self.end} through {self.transition}>'

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end and self.transition == other.transition
    



