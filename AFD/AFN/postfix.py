import sys  
import os
from BuilderEnum import BuilderEnum
sys.path.append(os.path.abspath(os.path.join("parsers")))
from stack import Stack

"""
Basado en https://www.free-online-calculator-use.com/infix-to-postfix-converter.html#
"""
class Postfixer:
    def __init__(self):
        self.stack = Stack()
        self.output = []
        self.enums = BuilderEnum
        self.precedence = {
            self.enums.KLEENE.value: 3,
            self.enums.PLUS.value: 3,
            self.enums.ASK.value: 3,
            self.enums.CONCAT.value: 2,
            self.enums.OR.value: 1,
        }
        self.checkOperands = 0
        self.operators = [
            self.enums.KLEENE.value, 
            self.enums.PLUS.value,
            self.enums.OR.value,
            self.enums.CONCAT.value,
            self.enums.ASK.value
        ]
    
    
    def is_operand(self, ch):
        if(ch not in self.operators) and ch != "(" and ch != ")":
            return True
        else: 
            return False

    def check_precedence(self, i):
        try:
            a = self.precedence[i]
            b = self.precedence[self.stack.peek()]
            return True if a <= b else False
        except KeyError:
            return False

    def get_symbol(self, expr):
        
        parens = False
        if expr[-1] == ")":
            parens = True

        stack = []

        index = -1
        for i in range(len(expr)-1,-1,-1):
            char = expr[i]
            if not parens:
                if self.is_operand(char) and char not in ["(", ")"]:
                    return i, char

            else:
                if char == ")":
                    stack.append(char)
                elif char == "(":
                    stack.pop()
                    if not stack:
                        index = i
                        return index, "(" + expr[i+1:]


    def fix_operators(self, expr):

        new = ""
        index = 0
        for i in range(len(expr)):
            if expr[i]==self.enums.PLUS.value:
                #obtenemos lo que este a la izq
                
                index, last = self.get_symbol(expr[:i])
                
                #left operator . left operator*
                add= last + last +"*"
                decider = expr[:i]
                if decider[-1] == ")":
                    new += add
                else:
                    new = new[:len(new) -1 ]
                    new += add
                
                
                continue
            elif expr[i]==self.enums.ASK.value:
                index, last = self.get_symbol(expr[:i])
                
                #left operator (r | e) 
                add="(" + last + "|" + "&"")"
                decider = expr[:i]
                if decider[-1] == ")":
                    new += add
                else:
                    new = new[:len(new) -1 ]
                    new += add
                
               
                
                continue
            if i+1< len(expr):
                if expr[i+1] != self.enums.ASK.value or expr[i+1] != self.enums.PLUS.value:
                    new += expr[i]
            else: 
                if expr[-1] != self.enums.ASK.value or expr[-1] != self.enums.PLUS.value:
                    new += expr[i]
    
        return new
        
    def fix_string(self, expr):
        expr = self.fix_operators(expr)
        fixed = ""
        posToInsert = []
        isOk = True
        pushStack = []
        for i in range(len(expr)-1):
            #si hay parens y no es operador...ni parentesis
            if(expr[i] == ")" and expr[i+1] not in self.operators and expr[i+1] != "(" and expr[i+1] != ")"):
                posToInsert.append(i)
            
            if(self.is_operand(expr[i]) and self.is_operand(expr[i+1])):
                
                posToInsert.append(i)
            if(expr[i] == "*" and expr[i+1] == "*"):
                isOk = False
            if len(pushStack)>0:
                last_elem = pushStack[-1]
                if last_elem == "*" and expr[i] == "*":
                    isOk = False
            if(expr[i] == "*" and expr[i+1] == ")"):
                pushStack.append(")")
                pushStack.append("*")
            
            if(expr[i] == "(") and (i != 0) and self.is_operand(expr[i-1]) and self.is_operand(expr[i+1]):
               
                posToInsert.append(i-1)

            if((expr[i] == "*" or expr[i] == "+") and self.is_operand(expr[i+1]) and (expr[i+1] != "(" or expr[i+1] != ")")):
                
                posToInsert.append(i)

            if((expr[i] == "*" or expr[i] == "+") and (expr[i-1] == ")" and expr[i+1]) == "("):
                posToInsert.append(i)

            if(expr[i] == "*" and expr[i+1] == "("):
                posToInsert.append(i)

            if(expr[i] == ")" and expr[i+1] == "("):
                posToInsert.append(i)

            if(expr[i] == "." and (not self.is_operand(expr[i+1]))):
                fixed += "&"

            if(isOk):
                fixed +=expr[i]
    
            isOk = True
        
        fixed +=expr[-1]
        if self.is_operand(expr[-1]):
            posToInsert.append(len(expr)-1)
        elif expr[-1] == self.enums.CONCAT.value or expr[-1] == self.enums.OR.value:
            fixed += "&"

        
        
        
        #sirve para llevar track del offser
        adder = 0
        for i in posToInsert:
            adder += 1
            fixed = list(fixed)
            fixed.insert(i+adder, self.enums.CONCAT.value)
            fixed = ''.join(fixed)
        
        if fixed[-1] == self.enums.CONCAT.value:
            return fixed[:len(fixed)-1]
        else:
            return fixed

    def to_postfix(self, expr):
        expr = self.fix_string(expr)
        
        print("INTERPRETING AS: ", expr)
        for ch in expr:
            if self.is_operand(ch):
                self.output.append(ch)

            elif ch == self.enums.LEFT_PARENS.value:
                
                self.stack.add(ch)

            elif ch == ")":
                
                
                while ((not self.stack.is_empty()) and (self.stack.peek() != self.enums.LEFT_PARENS.value)):
                    a = self.stack.pop()
                    self.output.append(a)

                if (not self.stack.is_empty() and self.stack.peek() != self.enums.LEFT_PARENS.value):
                    print("ERR: Incorrect syntax")
                    exit(-1)
                else:
                    self.stack.pop()
            
            elif ch in self.operators:
            
                while(not self.stack.is_empty() and self.check_precedence(ch)):
                    
                    self.output.append(self.stack.pop())

                self.stack.add(ch)
            #non supported char
            else:
                
                print("ERR: Incorrect syntax")

                print("NON SUPPORTED CHAR", ch)
                exit(-1)
                        
        while not self.stack.is_empty():
            self.output.append(self.stack.pop())
        
        return self.output
