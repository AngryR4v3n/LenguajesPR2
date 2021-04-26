from Builder import *
from Parser import Parser
from postfix import Postfixer
import sys  
import os
sys.path.append(os.path.abspath(os.path.join("AFD/AFN")))
from BuilderEnum import BuilderEnum
#should return tokens



def main():
    automata = input("Please type your RegEx: ") 
    res = generate("PowerSet", automata, False)

#toBuild = "AFD"
#automata = "(a|b)*abb"

def generate(toBuild, automata, paint): 
    postfixer = Postfixer()
    if(toBuild == "AFD"):
        inFixRegEx = "("+automata+")"
        inFixRegEx += ".#"
        inFixRegEx = postfixer.to_postfix(inFixRegEx)
        builder = Builder(inFixRegEx)
    else:
        postfixRegex = postfixer.to_postfix(automata)
        builder = Builder(postfixRegex)
    #paso de generar tokens
    builder.generator()
    #array de tokens devuelto por
    tokens = builder.getTokenArr()
    parser = Parser()

    return parser.parse(tokens, toBuild, paint)

def simulator(automata, isNfa):
    string = input("Type the string to test: ")
    print("Simulating: \n", automata)
    if isNfa:
        ans = automata.simulate_NFA(string)
        if ans > 0:
            print("yes")
        else: 
            print("no")
    else:
        ans = automata.simulate_DFA(string)
        if ans > 0:
            print("yes")
        else:
            print("no")

#main()
def single(regex, hashType):
    postfixer = Postfixer()
    postfixRegex = postfixer.to_postfix(f"({regex}).#")
    builder = Builder(postfixRegex)
    #paso de generar tokens
    builder.generator()
    #array de tokens devuelto por
    tokens = builder.getTokenArr()
    print("Tokens -> Regex:", tokens)
    parser = Parser()
    return parser.parse(tokens, "AFD", False, hashType)

def whole_regex(arrRegex, dictionary):
    main_tree = ""
    for regex in arrRegex:
        main_tree += "("+ regex + ")" + f"{BuilderEnum.CONCAT.value}{BuilderEnum.HASH.value}" + f"{BuilderEnum.OR.value}"
    #delete last or..
    main_tree = main_tree[0:-1]
    print("Main tree is: ", main_tree)
    postfixer = Postfixer()
    postfixRegex = postfixer.to_postfix(main_tree)
    builder = Builder(postfixRegex, dictionary=dictionary)
    #paso de generar tokens
    builder.generator()
    #array de tokens devuelto por
    tokens = builder.getTokenArr()
    print("Tokens -> Regex:", tokens)
    parser = Parser()
    return parser.parse(tokens, "AFD", True)
    
    
def test():
    postfixer = Postfixer()
    postfixRegex = postfixer.to_postfix(f'(((+)δ(-))γ"0γ1γ2γ3γ4γ5γ6γ7γ8γ9")("0γ1γ2γ3γ4γ5γ6γ7γ8γ9")αδ{BuilderEnum.HASH.value}')
    builder = Builder(postfixRegex)
    #paso de generar tokens
    builder.generator()
    #array de tokens devuelto por
    tokens = builder.getTokenArr()
    print("Tokens -> Regex:", tokens)
    parser = Parser()
    return parser.parse(tokens, "AFD", True)
    


