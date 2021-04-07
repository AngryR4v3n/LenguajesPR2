from stack import Stack
from BuilderEnum import BuilderEnum
from TreeInfo import *
class BTree:
    def __init__(self):
        #Structure
        self.left = None
        self.right = None
        self.root = None
        
        #logic
        self.number = None
        self.nullable = None
        self.first_pos = None
        self.last_pos = None
        self.forward_pos = None
        
    def set_number(self, number):
        self.number = number



    def compute_followpos(self, table):
        print(table)
        if self.root == ".":
            left = self.left.last_pos
            right = self.right.first_pos
           
            for i in left:
                for num in right:
                    if num not in table[i]:
                        table[i].append(num)
                    

                       

        elif self.root == "*":
            left = self.left.last_pos
            right = self.left.first_pos
           
            for i in left:
                for num in right:
                    if num not in table[i]:
                        table[i].append(num)
                        
                       

        #self.forward_pos = trans.get_end()


    def union( self, arr1, arr2):
        for elem in arr1:
            if elem not in arr2:
                arr2.append(elem)
        return arr2
    def __repr__(self):
        return f"<Tree Root: {self.root} right: {self.right} left:{self.left} \n first pos: {self.first_pos} last pos: {self.last_pos} follow pos {self.forward_pos}>"

def compute_positions(tree):
    
    f = compute_first(tree)
    l= compute_last(tree)
    
#recibe los tokens
def generate_tree(tokensArr):
    
    output = []
    stackOp = []
    counter = 0

    for token in tokensArr:
        #if its a symbol, we just add a tree with empty child
        if token.get_type() == "SYMBOL":
            tree = BTree()
            tree.root = token.get_value()
            tree.left = None
            tree.right = None
            tree.number = counter
            compute_positions(tree)
            stackOp.append(tree)
            counter += 1

        elif(token.get_type() != "SYMBOL"):
            if token.get_type() == "*":
                uniOp = stackOp.pop()
                tree = BTree()
                tree.root = token.get_type()
                tree.left = uniOp
                tree.right = None
                compute_positions(tree)
                stackOp.append(tree)
            

            #any other kind of operation of two operators ..
            
            else:
                op = token.get_type()
                rightOp = stackOp.pop()
                leftOp = stackOp.pop()
                tree = BTree()
                
                tree.root = op
                tree.left = leftOp
                tree.right = rightOp
                
                compute_positions(tree)

              
                stackOp.append(tree)
        
                
        
        
    

    return stackOp[-1]