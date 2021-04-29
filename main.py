from ATGReader import ATGReader
from ATGParser import ATGParser

words = open('./C.atg', "r").read().split("\n")
reader = ATGReader(words)

reader.build_atg()

#Conversion process
atgAutomatas = ATGParser(reader)

#Scanner writer
scanner = open("Scanner.py", "w")
imports = """import sys
import os
sys.path.append(os.path.abspath(os.path.join('AFD/AFN/parsers')))
from Automata import Automata
from Transition import Transition
"""
scanner.write(imports)

#Obtenemos automata..
#automata.states, automata.language, automata.start, automata.end, automata.fn
states, language, start, end, fn = atgAutomatas.main_tree()

#construimos automata en el scanner..
buildAutomata = f"""
automata = Automata({states},{language}, {start}, {end}, {fn})
"""
scanner.write(buildAutomata)
scanner.write("\n"*3)
reading = """f = open('test.txt', 'r')
def reader_tester():
    x = f.read()
    response = []
    r = automata.simulate_DFA(None, x[0])
    tokens = []
    x=x[1:]
    for c in x:
        if r:
            response.append(r)
            r = automata.simulate_DFA(response[-1], c)
            
        elif not r and len(response) > 0:
            tokens.append(response.pop())
            print("finished token", response)
            r= automata.simulate_DFA(None, c)

        else:
            break
    

    if r:
        response.append(r)
        r = automata.simulate_DFA(response[-1], c)
        
    elif not r and len(response) > 0:
        tokens.append(response.pop())
        r= automata.simulate_DFA(None, c)
        tokens.append(r)

    else: 
        print("No tokens.")
    if len(tokens) == 0 and len(response) > 0:
        tokens.append(response.pop())
    print("Finished", tokens)

    return tokens
    """

printer = """\n
def token_print(tokens):
    for token in tokens:
        name = token.type.keys()
        name = list(name)
        print(f"<Token w/id: {name}>")
"""
scanner.write(reading)
scanner.write(printer)
readerCall = """\nx = reader_tester()"""
printerCall = """\ntoken_print(x)"""
scanner.write(readerCall)
scanner.write(printerCall)


#atgAutomatas.convert_characters()
#atgAutomatas.convert_keywords()
#atgAutomatas.convert_tokens()
#atgAutomatas.test()

print("End parsing ATG")

