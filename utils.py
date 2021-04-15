import sys
import os
sys.path.append(os.path.abspath(os.path.join("AFD/AFN")))
from BuilderEnum import BuilderEnum

def find_all_positions(string, substring):
    res = [i for i in range(len(string)) if string.startswith(substring, i)]
    return res
"""
Identifies operands for + -
"""
def operands_identifier(value):
    count = 0
    opMode = False
    operators = ["+", "-"]
    toBeIdentified = []
    word = ""
    string = ""
    for char in value:
        if char == '"':
            count += 1
        if count % 2 == 0 and char != "." and char not in operators and char != " ":
            word += char
        if count % 2 != 0:
            string += char

        if char in operators:
            toBeIdentified.append(char)
            if string != "" and string != '"':
                string += '"'
                toBeIdentified.append(string)
            
            if word != "" and word != '"':
                toBeIdentified.append(word)
            
            word = ""
            string = ""

        
            
    if string != "" and string != '"':
                string += '"'
                toBeIdentified.append(string)
    if word != "" and word != '"':
        toBeIdentified.append(word)
            
    return toBeIdentified


def operands_identifier_v2(value):
    inOp = False
    operand = ""
    operator = ""
    start_op = ["{", "[", "("]
    close_op = ["}", "]", ")"]
    count = 0
    toBeIdentified = []
    for char in value:
        #agregamos primer operador 
        if char == '"':
            count += 1
        if char in start_op and count % 2 == 0:
            inOp = True

            if operand != "":
                
                toBeIdentified.append(operand)
                operand = ""

            
            operator = char
            toBeIdentified.append(operator)
            operator = ""

            

        elif char in close_op and count % 2 == 0:
            inOp = False
            if operand != "":
                
                toBeIdentified.append(operand)
                operand = ""
            
            operator = char
            toBeIdentified.append(operator)
            operator = ""
        else:
            inOp = False
        if not inOp and char and char not in close_op and char !=" ":
            operand += char

        elif not inOp and char and char != " " and count % 2 != 0:
            operand += char

        if operand == "EXCEPT":
            toBeIdentified.append(operand)
            operand = ""
    if len(operand) > 0:
        toBeIdentified.append(operand)
    return toBeIdentified
    

"""
Identifies if we are given a variable, it will replace that value
x = 'ola' -> 'ola'
"""
def identify_char(chars, diction):
    keys = diction.keys()
    for key in keys:
        if chars == key:
            return diction[key]

    #si posiciones esta vacia, es un operador. 
    positions = find_all_positions(chars, '"')
    if len(positions) > 0:
        if positions[0] == 0:
            positions[0] = 1
            chars = chars[positions[0]:positions[-1]]
        
            return chars
    else:
        return chars

"""
Here we evaluate strings that contain  op + op2. We evaluate and return a string 'abc'
INPUT: array of operands
OUTPUT: sentence already processed
"""
def evaluate_characters(array, mode):
    operations = ["+", "-", "{", "[", "("]

    stack = []
    toBeDone = []
    sentence = ""
    for operator in array:
        if operator not in operations:
            res = identify_char(operator, mode)
            res.replace('"', "")
            stack.append(res)
                
        else:   
            toBeDone.append(operator)
        
    #si es unitario, solo expulsamos lo que procesamos
    if len(toBeDone) == 0:
        return stack.pop()

    while len(toBeDone) > 0:
        
        op = toBeDone.pop().strip()
        
        
        if op == "-":
            second = stack.pop().strip().replace('"', "")
            first = stack.pop().strip().replace('"', "")

            sentence += first
            firstSet = set(first)
            secondSet = set(second)

            sentence = firstSet - secondSet
            sentence = sentence.pop()
            
        elif op == "+": 
            second = stack.pop().strip().replace('"', "")

            sentence += BuilderEnum.CONCAT.value
            sentence += second
            stack.append(sentence)

        elif op == "{":
            next_op = stack.pop(0)
            #jala todo lo que este dentro
            while next_op != "}":
                sentence += "(" + next_op +")"
                next_op = stack.pop(0)

            sentence += BuilderEnum.KLEENE.value
        elif op == "[":
            next_op = stack.pop(0)
            while next_op != "]":
                sentence += "(" + next_op +")"
                next_op = stack.pop(0)
            try:
                next_op = stack.pop(0)    
            except IndexError:
                next_op = "&"

            sentence += BuilderEnum.OR.value
            sentence += next_op

        elif op == "(":
            #encontramos el "("
            for i in range(len(array)):
                if array[i] == "(":
                    temp = i - 1
                    old_op = array[temp]
                    break
            
            if old_op:
                next_op = stack.pop(0)
                while next_op != ")":
                    sentence = sentence + old_op + next_op 
                    next_op = stack.pop(0)
            else:
                print("ERROR")

        while len(stack) > 0:
            sentence += stack.pop()


            




        return sentence