from BuilderEnum import BuilderEnum
import sys  
import os
#import dentro de la carpeta parsers
sys.path.append(os.path.abspath(os.path.join("parsers")))
from Transition import *
from Automata import Automata
import copy
from helper import * 
class PowerSet:
    def __init__(self):
        
        self.states = None
        self.language = None
        self.q0 = None
        self.final = None
        self.fn = None
        self.newfn = []
        self.counter = 0

        self.finalDFA = []

    def prepare(self, automata):
        self.states = automata.get_states()
        self.language = automata.get_language()
        self.q0 = automata.get_initial_state()
        self.final = automata.get_final_state()
        self.fn = automata.arr_states()
    
    def translate(self):
        vocab = vocabulary()
        diction = {}
        #iteramos para armar diccionario

        #en caso de overflow
        numb = len(self.newfn) - len(vocab) #un numero 30 digamos
        if numb > 0:
            for num in range(numb):
                vocab.append("Z"+str(num))

        for trans in self.newfn:
            if str(trans.get_start()) not in diction.keys():
                diction[str(trans.get_start())] = vocab[trans.index]
            
        #iteramos otra vez para traducir
        for trans in self.newfn:
            trans.set_start(diction[str(trans.get_start())])
            trans.set_end(diction[str(trans.get_end())])
        
    def subset_parser(self, auto, paint):
        self.prepare(auto)
        self.build_automata(automata=auto)
        # aqui deberiamos convertir todo..

        self.translate()
        initial = self.newfn[0]
        initial.set_initial(True)
        au = Automata([],[], initial, self.finalDFA, self.newfn)
        print("PowerSet AFD", au)
        #au.update_everything()
        if paint:
            export_chart_subset(au)
        
        return au

    def e_closure(self, states, res=[]):
        e_set = res
        for state in states:
            if state not in e_set:
                e_set.append(state)
        
        for transition in self.fn:
            for state in states:
                if transition.get_transition() == "&" and transition.get_start() == state and transition.get_end() not in e_set:
                    e_set.append(transition.get_end())
                    self.e_closure([transition.get_end()],res=e_set)
        
        return list(set(e_set))

    
    def traverse(self, state, letter):
        toReturn = []
        for i in state:
            for st in self.fn:
                if i == st.get_start() and st.get_transition() == letter:
                    toReturn.append(st.get_end())
                    break
        return toReturn
    
    def build_automata(self, checkArr=None, automata=None, counter=0):
        #revisamos las transiciones epsilon del start
        if checkArr == None:
            q0 = self.q0
            S = self.e_closure([q0])
            check = []
            dfa_states = []
            toState = Transition(start=S, transition=None, end=S)
            toState.set_initial(True)
            dfa_states.append(toState)
            check.append(toState)

        elif len(checkArr) > 0:
            S = []
            check = checkArr
            dfa_states = copy.copy(checkArr)

        else:
            print("SUBSET AFD", self.newfn)
            return "finished"
        #marcamos
        #self.mark_states(S)
        print("States", dfa_states)
    
        for toState in dfa_states:
            if toState.get_mark():
                continue
            toState.set_mark(True)
            #marcamos
            
            #obtenemos move de toState
            for letter in self.language:
                if letter != "&":
                    res = self.get_traversal(toState.get_end(), letter)
                    if len(res) > 0:
                        closure = self.e_closure(res, res=[])
                        closure.sort()
                        is_in_dfa = self.search_dfa_state(closure, check)
        
                    
                        if not is_in_dfa:
                            #Creamos y pusheamos el estado al array y al dfa
                            toPush_arr = Transition(start=toState.get_end(), transition=letter, end=closure)
                            toPush_arr.set_index(counter)
                            counter += 1 
                            if self.final in toPush_arr.get_start():
                                toPush_arr.set_final(True)
                                self.finalDFA.append(toPush_arr)
                            
                            self.newfn.append(toPush_arr)
                            check.append(toPush_arr)

                            
                    
                        else:
                            createState = Transition(start=toState.get_end(), transition=letter, end=closure)
                            createState.set_index(counter)
                            counter += 1 
                            if self.final in createState.get_start():
                                createState.set_final(True)
                            if not self.check_existence(createState):
                                self.newfn.append(createState)
            
        
        is_over = self.is_over(check)
        
        if not is_over:
            self.build_automata(checkArr=check, counter=counter)
        
        else:
            
            
            print("returning")
        
            return 
        #print("returning ", answer)
        
            
    
    def is_over(self, dfa):
        counter = 0
        for state in dfa:
            if state.get_mark():
                counter += 1
        
        if counter == len(dfa):
            return True
        else:
            return False


    #returns start of state if found in the array of transitions
    def search_dfa_state(self, dfa, stateList):
        
        for existing in stateList:
            if dfa == existing.get_end():
                    return existing.get_end()
        return None

    def check_existence(self, transition):
        for existing in self.newfn:
            if transition == existing:
                return True

        return False
        
    def get_traversal(self, arr, letter):
        answer = []
        subset = self.traverse(arr, letter)

        
        return list(set(subset))




    
        
        
    
        
    
        