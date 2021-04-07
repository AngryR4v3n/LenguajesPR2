

from BuilderEnum import BuilderEnum

#import dentro de la carpeta parsers
from Transition import *
from stack import Stack
from Automata import Automata
from helper import * 
class Thompson:
    def __init__(self):
        #array of states
        self.stateCounter = 0
        self.opStack = Stack()    
        self.nfa = []
    
    def evalPostfix(self, tokens):
        """
        Definimos las reglas segun: 
        https://medium.com/swlh/visualizing-thompsons-construction-algorithm-for-nfas-step-by-step-f92ef378581b 
        """
        
        for i in range(0, len(tokens)):
            
            currentToken = tokens[i]
            if currentToken.get_type() == "SYMBOL" and currentToken.get_value() == "&":
                #Regla #1: 
                #0 -> {1: "&"}
                trans1 = Transition(start=self.stateCounter, transition=currentToken.get_value(), end=self.stateCounter+1)
                self.stateCounter += 1
                #1 -> {} y es final.
                trans2 = Transition(start=self.stateCounter, transition=None, end=None)
                self.stateCounter += 1
                
                #estados, alfabeto, estado inicial, estado final, funcion de transicion
                au = Automata([], [], trans1.get_start(), trans2.get_start(), [])
                au.add_state(trans1)
                au.add_state(trans2)
                #print(au)
                #print("DONE &")
                self.opStack.add(au)

            elif currentToken.get_type() == "SYMBOL" and currentToken.get_value() != "&":
                #Regla #2: 
                #0 -> {1: "B"}
                trans1 = Transition(start=self.stateCounter, transition=currentToken.get_value(), end=self.stateCounter+1)
                self.stateCounter += 1
                #1 -> {} y es final.
                trans2 = Transition(start=self.stateCounter, transition=None, end=None)
                self.stateCounter += 1
                
                #estados, alfabeto, estado inicial, estado final, funcion de transicion
                au = Automata([], [], trans1.get_start(), trans2.get_start(), [])
                au.add_state(trans1)
                au.add_state(trans2)
                #print(au)
                #print("DONE SYMB")
                self.opStack.add(au)
                

            #sea una operacion
            elif currentToken.get_type() != "SYMBOL":

                #regla #3: OR
                if currentToken.get_type() == "|":
                    #sacamos del stack
                    nfa2 = self.opStack.pop()
                    
                    nfa1 = self.opStack.pop()

                    #armado de nfa base.
                    #TRANSICIONES
                    transitionInitial1 = Transition(start=self.stateCounter, transition="&", end=nfa1.get_initial_state())
                    transitionInitial2 = Transition(start=self.stateCounter, transition="&", end=nfa2.get_initial_state())
                    self.stateCounter += 1
                    transitionFinal1 = Transition(start=nfa1.get_final_state(), transition="&", end=self.stateCounter)
                    transitionFinal2 = Transition(start=nfa2.get_final_state(), transition="&", end=self.stateCounter)
                    self.stateCounter += 1

                    #Sacamos todas las transiciones del elem1 y elem2 
                    arr2 = nfa2.arr_states() #array
                    arr1 = nfa1.arr_states() #array
                    #unificamos los nfa
                    unifiedArray = arr2 + arr1
                    newTrans = [transitionInitial1, transitionInitial2, transitionFinal1, transitionFinal2]
                    finalTrans = unifiedArray + newTrans    
 
                    or_nfa = Automata([], [], transitionInitial1.get_start(), transitionFinal1.get_end(), [])
                    # me devuelve un array de States.
                    for transition in finalTrans:
                        if(transition.get_transition() != None):
                            or_nfa.add_state(transition)
                    
                    #print(or_nfa)
                    #print("DONE OR, to: \n", nfa2, "\n", nfa1 )
                    self.opStack.add(or_nfa)
                
                #REGLA KLEENE
                if currentToken.get_type() == "*":
                    nfa = self.opStack.pop()
                    
                    #encontramos estados finales e iniciales:
                    final = nfa.get_final_state()        
                    initial = nfa.get_initial_state()
                    #transicion de final a inicial del nfa preexistente
                    finalMod = Transition(start=final, transition="&", end=initial)

                    
                    
                    #estado inicial de nfa preexistente a nuevo estado de trans
                    initialState = Transition(self.stateCounter, "&",  initial)
                    
                    self.stateCounter += 1
                    
                    finalState = Transition(self.stateCounter, None, None)
                    initialEnd = Transition(initialState.get_start(), "&", finalState.get_start())
                    #transicion de nfa final a final de nuevo nfa
                    finalTofinal = Transition(start=final, transition="&", end=finalState.get_start())
                    
                    self.stateCounter += 1
                    
                    
                    kleene_nfa = Automata([], [], initialState.get_start(), finalState.get_start(), [])
                    arr1 = nfa.arr_states()
                    unifiedArray = arr1
                    newTrans = [initialState,initialEnd, finalState, finalTofinal, finalMod]
                    finalTrans = unifiedArray + newTrans
                    
                    for transition in finalTrans:
                        if(transition.get_transition() != None):
                            kleene_nfa.add_state(transition)

                    #print("DONE KLEENE to \n", nfa)
                    self.opStack.add(kleene_nfa)

                if currentToken.get_type() == "+":
                    nfa = self.opStack.pop()
                    
                    #encontramos estados finales e iniciales:
                    final = nfa.get_final_state()        
                    initial = nfa.get_initial_state()

                    target_symbol = None
                    for fn in nfa.arr_states():
                        if initial == fn.get_start():
                            target_symbol = fn.get_transition()
                            break
                    
                    
                    midState = Transition(self.stateCounter, transition="&", end=initial)
                    self.stateCounter += 1

                    cycle_state = Transition(self.stateCounter, transition=target_symbol, end=midState.get_start())
                    self.stateCounter += 1

                    
                    #transicion de final a inicial del nfa preexistente
                    finalMod = Transition(start=final, transition="&", end=initial)
                    
                    #estado inicial de nfa preexistente a nuevo estado de trans
                    
                    finalState = Transition(self.stateCounter, None, None)
                    self.stateCounter += 1
                    initialState = Transition(midState.get_start(), "&",  finalState.get_start())
                    
                    
                    #transicion de nfa final a final de nuevo nfa
                    finalTofinal = Transition(start=final, transition="&", end=finalState.get_start())
                    
                   
                    
                    
                    plus_nfa = Automata([], [], cycle_state.get_start(), finalState.get_start(), [])
                    arr1 = nfa.arr_states()
                    unifiedArray = arr1
                    newTrans = [initialState, finalState, finalTofinal, midState,cycle_state, finalMod]
                    finalTrans = unifiedArray + newTrans
                    
                    for transition in finalTrans:
                        if(transition.get_transition() != None):
                            plus_nfa.add_state(transition)

                    #print("DONE PLUS to: \n", nfa)
                    self.opStack.add(plus_nfa)


                if currentToken.get_type() == ".":
                    nfa2 = self.opStack.pop()
                    nfa1 = self.opStack.pop()

                    initial = nfa2.get_initial_state()
                    final = nfa1.get_final_state()
                    #print("INIT", initial)
                    #print("FINAL", final)
                    for state in nfa2.arr_states():
                        #print("STATE", state)
                        if (state.get_start() == initial):
                            state.set_start(final)

                    for state in nfa1.arr_states():
                        if(state.get_start() == final):
                            state.set_start(initial)
                    merge_nfa = Automata([], [], nfa1.get_initial_state(), nfa2.get_final_state(), [])

                    opsNfa2 = nfa2.arr_states()
                    opsNfa1 = nfa1.arr_states()

                    merged = opsNfa2 + opsNfa1

                    for transition in merged:
                        if(transition.get_transition() != None):
                            merge_nfa.add_state(transition)

                    #print(merge_nfa)
                    #print("DONE CONCAT to \n", nfa1, "\n", nfa2 )
                    self.opStack.add(merge_nfa)

        #opstack is ready to be exported
        return self.opStack

    def empty_stack(self, stack):
        merge_nfa = None
       
        while stack.length()<1:
            #lo tomamos como join 
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            initial = nfa2.get_initial_state()
            final = nfa1.get_final_state()
            #print("INIT", initial)
            #print("FINAL", final)
            for state in nfa2.arr_states():
                #print("STATE", state)
                if (state.get_start() == initial):
                    
                    state.set_start(final)

            for state in nfa1.arr_states():
                if(state.get_start() == final):
                    
                    state.set_start(initial)
            merge_nfa = Automata([], [], nfa1.get_initial_state(), nfa2.get_final_state(), [])

            opsNfa2 = nfa2.arr_states()
            opsNfa1 = nfa1.arr_states()

            merged = opsNfa2 + opsNfa1

            for transition in merged:
                if(transition.get_transition() != None):
                    merge_nfa.add_state(transition)
                
        if not merge_nfa:
            merge_nfa = self.opStack.pop()
        
        self.opStack.add(merge_nfa)
        
        
        return stack


    def thompson_parser(self, tokens, paint):
        #print("Hi, im being passed these tokens! \n", tokens)
        nfa = self.evalPostfix(tokens)
        nfa = self.empty_stack(nfa)
        #print("FINAL",nfa)
        res = nfa.pop()
        #print("RES", res)
        #export a imagen
        if paint:
            export_chart(res)
        return res
    
    def thompson_export(self, tokens):
        nfa = self.evalPostfix(tokens)
        nfa = self.empty_stack(nfa)
        res = nfa.pop()
        return res
        
        

                
