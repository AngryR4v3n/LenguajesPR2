import sys
import os
sys.path.append(os.path.abspath(os.path.join('AFD/AFN/parsers')))
from Automata import Automata
from Transition import Transition

automata = Automata([],['A', 'B', 'C', '0', '1', '2', 'ζ'], Transition([0, 1, 2, 10, 11, 12], "A",[3, 4, 5, 6, 7, 8, 9], {'ident': 9})
, [Transition([3, 4, 5, 6, 7, 8, 9], "None",None, {'ident': 9})
, Transition([3, 4, 5, 6, 7, 8, 9], "None",None, {'ident': 9})
, Transition([3, 4, 5, 6, 7, 8, 9], "None",None, {'ident': 9})
, Transition([16, 13, 14, 15], "None",None, {'number': 16})
, Transition([16, 13, 14, 15], "None",None, {'number': 16})
, Transition([16, 13, 14, 15], "None",None, {'number': 16})
, Transition([3, 4, 5, 6, 7, 8, 9], "None",None, {'ident': 9})
, Transition([3, 4, 5, 6, 7, 8, 9], "None",None, {'ident': 9})
, Transition([3, 4, 5, 6, 7, 8, 9], "None",None, {'ident': 9})
, Transition([3, 4, 5, 6, 7, 8, 9], "None",None, {'ident': 9})
, Transition([3, 4, 5, 6, 7, 8, 9], "None",None, {'ident': 9})
, Transition([3, 4, 5, 6, 7, 8, 9], "None",None, {'ident': 9})
, Transition([16, 13, 14, 15], "None",None, {'number': 16})
, Transition([16, 13, 14, 15], "None",None, {'number': 16})
, Transition([16, 13, 14, 15], "None",None, {'number': 16})
], [Transition([0, 1, 2, 10, 11, 12], "A",[3, 4, 5, 6, 7, 8, 9], {'ident': 9})
, Transition([0, 1, 2, 10, 11, 12], "B",[3, 4, 5, 6, 7, 8, 9], {'ident': 9})
, Transition([0, 1, 2, 10, 11, 12], "C",[3, 4, 5, 6, 7, 8, 9], {'ident': 9})
, Transition([0, 1, 2, 10, 11, 12], "0",[16, 13, 14, 15], {'number': 16})
, Transition([0, 1, 2, 10, 11, 12], "1",[16, 13, 14, 15], {'number': 16})
, Transition([0, 1, 2, 10, 11, 12], "2",[16, 13, 14, 15], {'number': 16})
, Transition([3, 4, 5, 6, 7, 8, 9], "A",[3, 4, 5, 6, 7, 8, 9], {'ident': 9})
, Transition([3, 4, 5, 6, 7, 8, 9], "B",[3, 4, 5, 6, 7, 8, 9], {'ident': 9})
, Transition([3, 4, 5, 6, 7, 8, 9], "C",[3, 4, 5, 6, 7, 8, 9], {'ident': 9})
, Transition([3, 4, 5, 6, 7, 8, 9], "0",[3, 4, 5, 6, 7, 8, 9], {'ident': 9})
, Transition([3, 4, 5, 6, 7, 8, 9], "1",[3, 4, 5, 6, 7, 8, 9], {'ident': 9})
, Transition([3, 4, 5, 6, 7, 8, 9], "2",[3, 4, 5, 6, 7, 8, 9], {'ident': 9})
, Transition([16, 13, 14, 15], "0",[16, 13, 14, 15], {'number': 16})
, Transition([16, 13, 14, 15], "1",[16, 13, 14, 15], {'number': 16})
, Transition([16, 13, 14, 15], "2",[16, 13, 14, 15], {'number': 16})
, Transition([3, 4, 5, 6, 7, 8, 9], "None",None, {'ident': 9})
, Transition([3, 4, 5, 6, 7, 8, 9], "None",None, {'ident': 9})
, Transition([3, 4, 5, 6, 7, 8, 9], "None",None, {'ident': 9})
, Transition([16, 13, 14, 15], "None",None, {'number': 16})
, Transition([16, 13, 14, 15], "None",None, {'number': 16})
, Transition([16, 13, 14, 15], "None",None, {'number': 16})
, Transition([3, 4, 5, 6, 7, 8, 9], "None",None, {'ident': 9})
, Transition([3, 4, 5, 6, 7, 8, 9], "None",None, {'ident': 9})
, Transition([3, 4, 5, 6, 7, 8, 9], "None",None, {'ident': 9})
, Transition([3, 4, 5, 6, 7, 8, 9], "None",None, {'ident': 9})
, Transition([3, 4, 5, 6, 7, 8, 9], "None",None, {'ident': 9})
, Transition([3, 4, 5, 6, 7, 8, 9], "None",None, {'ident': 9})
, Transition([16, 13, 14, 15], "None",None, {'number': 16})
, Transition([16, 13, 14, 15], "None",None, {'number': 16})
, Transition([16, 13, 14, 15], "None",None, {'number': 16})
])



f = open('test.txt', 'r')
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
            
        else:
            tokens.append(response.pop())
            print("finished token", response)
            r= automata.simulate_DFA(None, c)
    

    if r:
        response.append(r)
        r = automata.simulate_DFA(response[-1], c)
        
    else:
        tokens.append(response.pop())
        r= automata.simulate_DFA(None, c)
        tokens.append(r)
    if len(tokens) == 0:
        tokens.append(response.pop())
    print("Finished", tokens)
    
reader_tester()