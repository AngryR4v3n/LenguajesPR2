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
tokens = {reader.tokens}
"""
scanner.write(buildAutomata)
scanner.write("\n"*3)
reading = """f = open('test.txt', 'r')

def reader_tester():
    x = f.read()
    pos = 0
    while pos < len(x):
        resultado, pos, aceptacion = automata.simulate_DFA(x, pos)
        if aceptacion:
            allowed = True

            if allowed:
                print(" ->  ",repr(resultado), "identified", list(aceptacion.type.keys())[0], " <-")
        else:
            print(" ->  ",repr(resultado), "unidentified string of chars <-")
        
    

x = reader_tester()    """
scanner.write(reading)
readerCall = """\nx = reader_tester()"""
scanner.write(readerCall)


#atgAutomatas.convert_characters()
#atgAutomatas.convert_keywords()
#atgAutomatas.convert_tokens()
#atgAutomatas.test()

print("End parsing ATG")

