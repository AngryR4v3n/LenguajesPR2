import sys
import os
sys.path.append(os.path.abspath(os.path.join("AFD/AFN")))
from BuilderEnum import BuilderEnum

def find_all_positions(string, substring):
    res = [i for i in range(len(string)) if string.startswith(substring, i)]
    return res

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
        #return self.to_regex(chars, 1)
            return chars
    else:
        return chars

"""
Here we evaluate strings that contain  op + op2. We evaluate and return a string 'abc'
INPUT: array of operands
OUTPUT: sentence already processed
"""
def evaluate_characters(array, mode):
    operations = ["+", "-"]
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
        second = stack.pop().strip().replace('"', "")
        first = stack.pop().strip().replace('"', "")
        op = toBeDone.pop().strip()
        sentence += first
        
        if op == "-":
            firstSet = set(first)
            secondSet = set(second)

            sentence = firstSet - secondSet
            sentence = sentence.pop()
            
        else: 
            sentence += BuilderEnum.CONCAT.value
            sentence += second
            stack.append(sentence)

        return sentence