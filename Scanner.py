import sys
import os
sys.path.append(os.path.abspath(os.path.join('AFD/AFN/parsers')))
from Automata import Automata
from Transition import Transition

automata = Automata([],['0', '1', '2', '3', 'A', 'B', 'C', 'D', 'E', 'F', 'H', 'ζ'], Transition([0, 1, 2, 3, 22, 23, 24, 25], "0",[4, 5, 6, 7, 8, 9, 26, 27, 28, 29], None)
, [Transition([30], "None",None, {'number': 30})
, Transition([30], "None",None, {'number': 30})
, Transition([30], "None",None, {'number': 30})
, Transition([30], "None",None, {'number': 30})
, Transition([21], "None",None, {'hexnumber': 21})
], [Transition([0, 1, 2, 3, 22, 23, 24, 25], "0",[4, 5, 6, 7, 8, 9, 26, 27, 28, 29], None)
, Transition([0, 1, 2, 3, 22, 23, 24, 25], "1",[4, 5, 6, 7, 8, 9, 26, 27, 28, 29], None)
, Transition([0, 1, 2, 3, 22, 23, 24, 25], "2",[4, 5, 6, 7, 8, 9, 26, 27, 28, 29], None)
, Transition([0, 1, 2, 3, 22, 23, 24, 25], "3",[4, 5, 6, 7, 8, 9, 26, 27, 28, 29], None)
, Transition([4, 5, 6, 7, 8, 9, 26, 27, 28, 29], "0",[30], {'number': 30})
, Transition([4, 5, 6, 7, 8, 9, 26, 27, 28, 29], "1",[30], {'number': 30})
, Transition([4, 5, 6, 7, 8, 9, 26, 27, 28, 29], "2",[30], {'number': 30})
, Transition([4, 5, 6, 7, 8, 9, 26, 27, 28, 29], "3",[30], {'number': 30})
, Transition([4, 5, 6, 7, 8, 9, 26, 27, 28, 29], "A",[10, 11, 12, 13, 20], None)
, Transition([4, 5, 6, 7, 8, 9, 26, 27, 28, 29], "B",[10, 11, 12, 13, 20], None)
, Transition([4, 5, 6, 7, 8, 9, 26, 27, 28, 29], "C",[10, 11, 12, 13, 20], None)
, Transition([4, 5, 6, 7, 8, 9, 26, 27, 28, 29], "D",[10, 11, 12, 13, 20], None)
, Transition([4, 5, 6, 7, 8, 9, 26, 27, 28, 29], "E",[10, 11, 12, 13, 20], None)
, Transition([4, 5, 6, 7, 8, 9, 26, 27, 28, 29], "F",[10, 11, 12, 13, 20], None)
, Transition([10, 11, 12, 13, 20], "0",[14, 15, 16, 17, 18, 19], None)
, Transition([10, 11, 12, 13, 20], "1",[14, 15, 16, 17, 18, 19], None)
, Transition([10, 11, 12, 13, 20], "2",[14, 15, 16, 17, 18, 19], None)
, Transition([10, 11, 12, 13, 20], "3",[14, 15, 16, 17, 18, 19], None)
, Transition([10, 11, 12, 13, 20], "H",[21], {'hexnumber': 21})
, Transition([14, 15, 16, 17, 18, 19], "A",[10, 11, 12, 13, 20], None)
, Transition([14, 15, 16, 17, 18, 19], "B",[10, 11, 12, 13, 20], None)
, Transition([14, 15, 16, 17, 18, 19], "C",[10, 11, 12, 13, 20], None)
, Transition([14, 15, 16, 17, 18, 19], "D",[10, 11, 12, 13, 20], None)
, Transition([14, 15, 16, 17, 18, 19], "E",[10, 11, 12, 13, 20], None)
, Transition([14, 15, 16, 17, 18, 19], "F",[10, 11, 12, 13, 20], None)
, Transition([30], "None",None, {'number': 30})
, Transition([30], "None",None, {'number': 30})
, Transition([30], "None",None, {'number': 30})
, Transition([30], "None",None, {'number': 30})
, Transition([21], "None",None, {'hexnumber': 21})
])



f = open('test.txt', 'r')
    x = f.read()
    response = []
    r = automata.simulate_DFA(None, x[0])
    x=x[1:]
    for c in x:
        if r:
            response.append(r)
            r = automata.simulate_DFA(response[-1], c)
        else:
            print("finished token", response)
            r= automata.simulate_DFA(None, c)
            
    #el ultimo..
    response.append(r)

    print("Finished", response)
    
reader_tester()