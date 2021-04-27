from BuilderEnum import BuilderEnum
from BT import *
from TreeInfo import *
from Transition import Transition
from Automata import Automata
import copy
from helper import *
class AFD:
    def __init__(self, kind="None"):
        self.fn = []
        self.initial = None
        self.final = None
        self.translator = None
        self.table = []
        self.finalDFA = []
        self.language = []
        self.type = kind

    def tree_to_stack(self, tree, res=[]):
        if tree:
            res.append(tree)
        if tree.left:
            self.tree_to_stack(tree.left, res=res)
        if tree.right:
            self.tree_to_stack(tree.right, res=res)
      
        return res
        
    def fix_tokens(self,tokens):
        new_tokens = []
        popNext = False
        add = True
        for i in range(len(tokens)-1):
            add = True
            
            if tokens[i].get_value() == "&":
                add = False
                if (tokens[i+1].get_type() == BuilderEnum.CONCAT.value or tokens[i+1].get_type() == BuilderEnum.OR.value):
                    popNext = True
                    continue
                    
            if add:
                new_tokens.append(tokens[i])
            
            if popNext:
                new_tokens.pop()
                popNext = False


        new_tokens.append(tokens[-1])
        return new_tokens


    def get_hashtags(self, st):
        finalDict = {}
        for elem in st:
            if elem.root == BuilderEnum.HASH.value:
                finalDict[elem.first_pos[0]]=elem.identifier

        return finalDict
    def afd_parser(self, rawToken, paint):
        
        tokens = self.fix_tokens(rawToken)
        #print("Hi, im being passed this tokens! \n", tokens)
        tree = generate_tree(tokens)
        st = self.tree_to_stack(tree, [])
        st.reverse()
        table = self.compute_positions(st)
        #we turn it around to have depth first..

        self.final = self.get_hashtags(st)
        st.reverse()
        self.initial = st[0].first_pos
        self.createDFA(tokens)
        #self.translate()
        
        #print("STATES", self.fn)
        initial = self.fn[0]
        initial.set_initial(True)
        au = Automata([], self.language, initial, self.finalDFA, self.fn)
        print("automata", au)

        if paint:
            export_chart_subset(au)
        
        return au
        

    def translate(self):
        vocab = vocabulary()
        diction = {}
        #iteramos para armar diccionario
        numb = len(self.fn) - len(vocab) #un numero 30 digamos
        if numb > 0:
            for num in range(numb):
                vocab.append("Z"+str(num))

        for trans in self.fn:
            if str(trans.get_start()) not in diction.keys():
                if trans.index != None:
                    diction[str(trans.get_start())] = vocab[trans.index]
        #iteramos otra vez para traducir
        for trans in self.fn:
            if trans.transition:
                trans.set_start(diction[str(trans.get_start())])
                trans.set_end(diction[str(trans.get_end())])


    def compute_positions(self, stackTree):
        counter = 0
        #preparamos tabla
        table = []
        #[[0, 1, 2], [0, 1, 2], [3] ..]
        for tree in stackTree:
            if tree.number != None:
                table.append([])
                
        #primero todos los finales
        translator = {}    
        
        for elem in stackTree:
           
            if elem.number != None:        
                #translate
                if elem.root not in translator.keys():
                    translator[elem.root] = [elem.number]
                else:
                    translator[elem.root].append(elem.number)
                
        #ahora las ops 
        counter = 0
        for elem in stackTree:
            #FIRST POS
            if elem.number == None:
                #LAST POS
                elem.compute_followpos(table)
            
            counter += 1

        
        self.translator = translator
        self.table = table

        
        return table

    def interset(self, arr1, arr2):
        res = []
        arr1 = list(arr1)
        if arr2:
            if len(arr1) >= len(arr2):
                setA = arr1
                setB = arr2
            else:
                setA = arr2
                setB = arr1

            for elemB in setB:
                for elemA in setA:
                    if elemA == elemB:
                        res.append(elemA)

        if res:
            return res, True
        else:
            return res, False
        return res

    def createDFA(self, tokens):
        language = []
        for token in tokens:
            if token.get_type() == "SYMBOL" and (token.get_value() != "&"):
                if token.get_value() not in language:
                    language.append(token.get_value())
        self.language = language
        self.build_automata(language)
        
        for x in self.fn:
            #if self.final in x.get_end():
            z, isCommon = self.interset(self.final.keys(), x.get_end())
            if isCommon:
                #creamos estado nuevo
                
                f = Transition(start=x.get_end(), transition=None, end=None, kind={self.final[z[0]]: z[0]})
                f.set_final(True)
                self.fn.append(f)
                self.finalDFA.append(f)
                
                arr = self.find_transition_to_end(x.get_end())
                for i in arr:
                    i.type = {self.final[z[0]]: z[0]}
                
        return

    def find_transition_to_end(self, end):
        res = []
        for x in self.fn:
            if x.get_end() == end:
                res.append(x)

        return res
    
   
    def build_automata(self, language, counter=0, checkArr=None):
        if checkArr == None:
            q0 = self.initial
            check = []
            dfa_states = []
            toState = Transition(start=q0, transition=None, end=q0)
            toState.set_initial(True)
            dfa_states.append(toState)
            #check.append(toState)

        elif len(checkArr) > 0:
            S = []
            check = checkArr
            dfa_states = copy.copy(checkArr)
            
        else:
            print("AFD", check)
            return "finished"
        #print("States", dfa_states)
    
        for toState in dfa_states:
            if toState.get_mark():
                #toState = dfa_states.pop()
                continue
            toState.set_mark(True)
            #marcamos
            
            #obtenemos move de toState
            for letter in language:
                if letter != "&" and letter != BuilderEnum.HASH.value:
                    #get traversal pasa a ser la union de los follow pos de cada uno de los elem
                    res = self.traverse(toState.get_end(), letter)
                    if len(res) > 0:
                        is_in_dfa = self.search_dfa_state(res, check)
                    
                        if not is_in_dfa:
                            #Creamos y pusheamos el estado al array y al dfa
                            toPush_arr = Transition(start=toState.get_end(), transition=letter, end=res)
                            toPush_arr.set_index(counter)
                            counter += 1 
                            self.fn.append(toPush_arr)
                            check.append(toPush_arr)       
                    
                        else:
                            createState = Transition(start=toState.get_end(), transition=letter, end=res)
                            createState.set_index(counter)
                            counter += 1 
                            if not self.check_existence(createState):
                                self.fn.append(createState)      
                else:
                    continue
        
        is_over = self.is_over(check)
        
        if not is_over:
            self.build_automata(checkArr=check, language=language ,counter=counter)
        else:
            #print("TRANS",self.fn)
            return "finished"


    def change_translator(self, value):
        for key, values in self.translator.items():
            if value in values:
                return key

    def traverse(self, state, letter):
        toReturn = []
        #obtenemos los follow pos
        for elem in state:        
            #obtenemos letra
            letra = self.change_translator(elem)
            if letra == letter:
                toReturn += self.table[elem]
    
        return list(set(toReturn))
    

    def search_dfa_state(self, state, stateRepo):
        for existing in stateRepo:
            if state == existing.get_end():
                return True
                break
        return False


    def check_existence(self, transition):
        for existing in self.fn:
            if transition == existing:
                return True

        return False
            
    def is_over(self, dfa):
        counter = 0
        for state in dfa:
            if state.get_mark():
                counter += 1
        
        if counter == len(dfa):
            return True
        else:
            return False
