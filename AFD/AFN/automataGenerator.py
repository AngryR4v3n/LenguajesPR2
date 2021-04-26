from Builder import *
from Parser import Parser
from postfix import Postfixer
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

def test():
    postfixer = Postfixer()
    postfixRegex = postfixer.to_postfix('(("|"|1|2|3|4|5|6|7|8|9)).#')
    builder = Builder(postfixRegex)
    #paso de generar tokens
    builder.generator()
    #array de tokens devuelto por
    tokens = builder.getTokenArr()
    print("Tokens -> Regex:", tokens)
    parser = Parser()
    return parser.parse(tokens, "AFD", True)
    


