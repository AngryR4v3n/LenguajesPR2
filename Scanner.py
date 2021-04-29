import sys
import os
sys.path.append(os.path.abspath(os.path.join('AFD/AFN/parsers')))
from Automata import Automata
from Transition import Transition

automata = Automata([],['0', '1', '2', 'A', 'B', 'C', 'D', 'E', 'F', 'H', 'ζ', '\r', '\n', '\t'], Transition([0, 1, 2, 3, 4, 5, 6, 7, 8, 20, 21, 22, 23], '0',[9, 10, 11, 12, 13, 14, 15, 16, 17, 18], None)
, [Transition([24, 25, 26, 27, 28], None,None, {'whitetoken': 28})
, Transition([24, 25, 26, 27, 28], None,None, {'whitetoken': 28})
, Transition([24, 25, 26, 27, 28], None,None, {'whitetoken': 28})
, Transition([19], None,None, {'hexnumber': 19})
, Transition([24, 25, 26, 27, 28], None,None, {'whitetoken': 28})
, Transition([24, 25, 26, 27, 28], None,None, {'whitetoken': 28})
, Transition([24, 25, 26, 27, 28], None,None, {'whitetoken': 28})
], [Transition([0, 1, 2, 3, 4, 5, 6, 7, 8, 20, 21, 22, 23], '0',[9, 10, 11, 12, 13, 14, 15, 16, 17, 18], None)
, Transition([0, 1, 2, 3, 4, 5, 6, 7, 8, 20, 21, 22, 23], '1',[9, 10, 11, 12, 13, 14, 15, 16, 17, 18], None)
, Transition([0, 1, 2, 3, 4, 5, 6, 7, 8, 20, 21, 22, 23], '2',[9, 10, 11, 12, 13, 14, 15, 16, 17, 18], None)
, Transition([0, 1, 2, 3, 4, 5, 6, 7, 8, 20, 21, 22, 23], 'A',[9, 10, 11, 12, 13, 14, 15, 16, 17, 18], None)
, Transition([0, 1, 2, 3, 4, 5, 6, 7, 8, 20, 21, 22, 23], 'B',[9, 10, 11, 12, 13, 14, 15, 16, 17, 18], None)
, Transition([0, 1, 2, 3, 4, 5, 6, 7, 8, 20, 21, 22, 23], 'C',[9, 10, 11, 12, 13, 14, 15, 16, 17, 18], None)
, Transition([0, 1, 2, 3, 4, 5, 6, 7, 8, 20, 21, 22, 23], 'D',[9, 10, 11, 12, 13, 14, 15, 16, 17, 18], None)
, Transition([0, 1, 2, 3, 4, 5, 6, 7, 8, 20, 21, 22, 23], 'E',[9, 10, 11, 12, 13, 14, 15, 16, 17, 18], None)
, Transition([0, 1, 2, 3, 4, 5, 6, 7, 8, 20, 21, 22, 23], 'F',[9, 10, 11, 12, 13, 14, 15, 16, 17, 18], None)
, Transition([0, 1, 2, 3, 4, 5, 6, 7, 8, 20, 21, 22, 23], '\r',[24, 25, 26, 27, 28], {'whitetoken': 28})
, Transition([0, 1, 2, 3, 4, 5, 6, 7, 8, 20, 21, 22, 23], '\n',[24, 25, 26, 27, 28], {'whitetoken': 28})
, Transition([0, 1, 2, 3, 4, 5, 6, 7, 8, 20, 21, 22, 23], '\t',[24, 25, 26, 27, 28], {'whitetoken': 28})
, Transition([9, 10, 11, 12, 13, 14, 15, 16, 17, 18], '0',[9, 10, 11, 12, 13, 14, 15, 16, 17, 18], None)
, Transition([9, 10, 11, 12, 13, 14, 15, 16, 17, 18], '1',[9, 10, 11, 12, 13, 14, 15, 16, 17, 18], None)
, Transition([9, 10, 11, 12, 13, 14, 15, 16, 17, 18], '2',[9, 10, 11, 12, 13, 14, 15, 16, 17, 18], None)
, Transition([9, 10, 11, 12, 13, 14, 15, 16, 17, 18], 'A',[9, 10, 11, 12, 13, 14, 15, 16, 17, 18], None)
, Transition([9, 10, 11, 12, 13, 14, 15, 16, 17, 18], 'B',[9, 10, 11, 12, 13, 14, 15, 16, 17, 18], None)
, Transition([9, 10, 11, 12, 13, 14, 15, 16, 17, 18], 'C',[9, 10, 11, 12, 13, 14, 15, 16, 17, 18], None)
, Transition([9, 10, 11, 12, 13, 14, 15, 16, 17, 18], 'D',[9, 10, 11, 12, 13, 14, 15, 16, 17, 18], None)
, Transition([9, 10, 11, 12, 13, 14, 15, 16, 17, 18], 'E',[9, 10, 11, 12, 13, 14, 15, 16, 17, 18], None)
, Transition([9, 10, 11, 12, 13, 14, 15, 16, 17, 18], 'F',[9, 10, 11, 12, 13, 14, 15, 16, 17, 18], None)
, Transition([9, 10, 11, 12, 13, 14, 15, 16, 17, 18], 'H',[19], {'hexnumber': 19})
, Transition([24, 25, 26, 27, 28], '\r',[24, 25, 26, 27, 28], {'whitetoken': 28})
, Transition([24, 25, 26, 27, 28], '\n',[24, 25, 26, 27, 28], {'whitetoken': 28})
, Transition([24, 25, 26, 27, 28], '\t',[24, 25, 26, 27, 28], {'whitetoken': 28})
, Transition([24, 25, 26, 27, 28], None,None, {'whitetoken': 28})
, Transition([24, 25, 26, 27, 28], None,None, {'whitetoken': 28})
, Transition([24, 25, 26, 27, 28], None,None, {'whitetoken': 28})
, Transition([19], None,None, {'hexnumber': 19})
, Transition([24, 25, 26, 27, 28], None,None, {'whitetoken': 28})
, Transition([24, 25, 26, 27, 28], None,None, {'whitetoken': 28})
, Transition([24, 25, 26, 27, 28], None,None, {'whitetoken': 28})
])



f = open('test.txt', 'r')
def reader_tester():
    x = f.read()
    response = []
    r = automata.simulate_DFA(None, repr(x[0]))
    tokens = []
    x=x[1:]
    for c in x:
        c = repr(c)
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
    
reader_tester()