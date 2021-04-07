class Automata:
    def __init__(self, states, language, start, end, fn):
        #array of id states.
        self.states = states
        #Array of symbols
        self.language = language
        #start state obj of the automata
        self.start = start
        #end state
        self.end = end
        #fn is the array of transitions
        self.fn = fn
        #actual state (state obj)
        self.actualState = None


    def get_states(self):
        return self.states

    def get_language(self):
        return self.language
    
    def get_initial_state(self):
        return self.start

    def get_final_state(self):
        return self.end

    def set_initial_state(self, number):
        self.start = number

    def set_final_state(self, number):
        self.end = number

    def arr_states(self):
        return self.fn

    def add_state(self, trans):
        #extraemos los ids
        if trans.get_start() not in self.states:
            self.states.append(trans.get_start())

        if trans.get_end() not in self.states:
            self.states.append(trans.get_end())
        #agregamos a las funciones
        self.fn.append(trans)
        #agregamos a lenguaje
        if trans.get_transition() not in self.language and trans.get_transition() != None:
            self.language.append(trans.get_transition())


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
        return list(set(toReturn))


    def traverse_dfa(self, state, letter):
        toReturn = "bad"
        for st in self.fn:
            if st.get_start() == state and st.get_transition() == letter:
                toReturn = st.get_end()
        return toReturn

    def get_traversal(self, arr, letter):
        answer = []
        subset = self.traverse(arr, letter)

        
        return list(set(subset))

    def simulate_NFA(self, string):
        S = self.e_closure([self.start])

        for c in string:
            S = self.e_closure(self.get_traversal(S, c))

        if self.end in S:
            return 1
        else: 
            return 0

        print(S)
    
    def simulate_DFA(self, string):
        S = self.start
        for c in string:
            S = self.traverse_dfa(S,c)

        for elem in self.end:
            if S in elem.get_start():
                return 1
            else:
                return 0
        
    def __repr__(self):
        return f"\n<Automata fn: {self.fn} with language: {self.language} states: {self.states}>\n STARTING NODE: {self.start}, END STATES: {self.end}"
        
        

            