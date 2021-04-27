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
reading = """def reader_tester():
    f = open('test.txt', 'r')
    x = f.read()
    for c in x:
        r = automata.simulate_DFA(None, c)
    print("Finished", r)
    """


scanner.write(reading)
readerCall = """\nreader_tester()"""
scanner.write(readerCall)


#atgAutomatas.convert_characters()
#atgAutomatas.convert_keywords()
#atgAutomatas.convert_tokens()
#atgAutomatas.test()

print("End parsing ATG")

