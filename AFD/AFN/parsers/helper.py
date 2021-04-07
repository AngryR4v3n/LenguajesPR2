from graphviz import Digraph

"""
Example extracted from: https://graphviz.readthedocs.io/en/stable/examples.html#fsm-py
"""
def export_chart(nfa):
    f = Digraph('finite_state_machine', filename='nfa.gv')
    f.attr(rankdir='LR', size='8,5')
    f.attr('node', shape='rectangular')
    f.node(str(nfa.get_initial_state()))
    f.attr('node', shape='doublecircle')
    f.node(str(nfa.get_final_state()))

    f.attr('node', shape='circle')
    for transition in nfa.arr_states():
        f.edge(str(transition.get_start()), str(transition.get_end()), label=str(transition.get_transition()))
    
    f.view()

def export_chart_subset(dfa):
    f = Digraph('finite_state_machine', filename='dfa_subset.gv')
    f.attr(rankdir='LR', size='8,5')
    #extraemos inicial
    states_fn = dfa.arr_states()
    counter = 0
    f.attr('node', shape='rectangular')
    f.node(str(dfa.start.get_start()))
    
    
    f.attr('node', shape='doublecircle')
    for transition in states_fn:
        if transition.isFinal:
            f.node(str(transition.get_start()))
            #states_fn.remove(counter)
    

    f.attr('node', shape='circle')
    for transition in states_fn:
        f.edge(str(transition.get_start()), str(transition.get_end()), label=str(transition.get_transition()))

    f.view()
    

def vocabulary():
    arr = [
        "A", "B", "C", "D", "E", "F", "G", "H", 
        "I", "J", "K", "L", "M", "N", "O", "P", "Q",
        "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
    ]
    return arr

