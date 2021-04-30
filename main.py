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
keywords = {reader.keywords}
ignoreChars = {reader.ignore}
"""
scanner.write(buildAutomata)
scanner.write("\n"*3)


keysearch = """\n
def keyword_search(string):
    for elem in keywords.keys():
        if string == elem:
            return elem
    return None\n"""
scanner.write(keysearch)

reading = """f = open('test.txt', 'r')

def reader_tester():
    x = f.read()
    pos = 0
    while pos < len(x):
        resultado, pos, aceptacion = automata.simulate_DFA(x, pos, ignoreChars)
        if aceptacion:
            allowed = True

            if allowed:
                identifier = list(aceptacion.type.keys())[0]
                #obtenemos el token
                tkk = tokens[identifier]
                #buscamos en los keywords
                if tkk["isExcept"]:
                    key=keyword_search(resultado)
                    if key:
                        print(" ->  ",repr(resultado), "identified keyword", key, " <-")
                    else:
                        print(" ->  ",repr(resultado), "identified", identifier, " <-")
                else:    
                    print(" ->  ",repr(resultado), "identified", identifier, " <-")
        else:
            print(" ->  ",repr(resultado), "unidentified string of chars <-")
    

x = reader_tester()    """
scanner.write(reading)




#atgAutomatas.convert_characters()
#atgAutomatas.convert_keywords()
#atgAutomatas.convert_tokens()
#atgAutomatas.test()

print("End parsing ATG")

