import utils
import sys  
import os

sys.path.append(os.path.abspath(os.path.join("AFD/AFN")))
from BuilderEnum import BuilderEnum

class ATGReader():
    """
    Instantiates the ATG info extractor class.
    PARAMS: 
        file -> The raw file's content.
    """
    def __init__(self, file):
        self.words = file
        self.characters = {}
        self.keywords = {}
        self.productions = []
        self.tokens = []
        self.compilerName = ""
        self.counter = 0


    def read(self):
       for line in self.words:
            individual = line.split()
            if len(individual) > 0:
                if individual[0] == "COMPILER":
                    #execute compiler name module
                    self.compiler_name(self.words[self.counter])

                elif individual[0] == "CHARACTERS":
                    self.get_characters("CHARACTERS", "KEYWORDS")

                elif individual[0] == "KEYWORDS":
                    self.get_characters("KEYWORDS", "TOKENS")
                
                elif individual[0] == "TOKENS":
                    #self.get_tokens(self.words[self.counter])
                    print("doofus")

                #probably a comment or sth else ...


            self.counter += 1 

    """
    Builds and gets properties of the ATG. e.g: compiler, characters...
    PARAMS: 
        self -> the class
    """
    def build_atg(self):
        self.read()
    
    
    """
    Gets the compiler name from the ATG file, and modifies compilerName property.
    PARAMS: 
        self -> the class.
    """
    def compiler_name(self, line):
        self.compilerName = line.split()[1]


    """
    Gets the characters and interprets CHR() statements, replaces to the actual value
    PARAMS:
        self-> the class.
    """
    def get_characters(self, parsing, limit):
    
        elapsed_cycles = 0
        #revisamos donde estamos
        currentLine = self.words[self.counter]
        #mientras no lleguemos a seccion de tokens...
        while self.counter < len(self.words):
            
            self.counter += 1
            elapsed_cycles += 1
            #limpiamos de caracteres vacios al inicio o final
            currentLine = self.words[self.counter].strip()

            if len(currentLine) > 0:
                
                if currentLine.split()[0] == limit:
                    self.counter = self.counter - elapsed_cycles
                    break
                    #chequeamos estructura gramatical
                    
                result = self.line_grammar_check(currentLine)

                if result != None:

                    #agregamos segun sea el caso
                    if parsing == "CHARACTERS":    
                        self.characters[result[0]] = result[1]

                    elif parsing == "TOKENS":
                        self.tokens[result[0]] = result[1]

                    elif parsing == "KEYWORDS":
                        self.keywords[result[0]] = result[1]
                else:
                    print(f"Grammar error in {parsing} section - in line: ", self.counter)
                    break

        print(f"Finished {parsing}: Syntax is correct up to here :)")
        
        if parsing == "CHARACTERS":
            self.char_to_regex()

        elif parsing == "TOKENS":
            print("doofus")
            
        elif parsing == "KEYWORDS":
            self.keyword_to_regex()


    def line_grammar_check(self, currentLine):
        #revisamos que todo nice en gramatica, que exista un igual y que el final sea un . 
        if "=" in currentLine and currentLine[-1] == "." and currentLine != "": 
            split = currentLine.split("=")
            
            #removemos espacios... 
            cleanSplit = []
            for word in split:
                cleanSplit.append(word.strip())

            #chequeamos que si es CHAR(), lo pasamos de una..
            if cleanSplit[1].find("CHR(") > -1:
                converted = self.chr_interpreter(cleanSplit[1])
                cleanSplit[1] = converted

            if cleanSplit[1][-1] == ".":
                cleanSplit[1] = cleanSplit[1][0:-1]

        else:
            return None

        return cleanSplit

        

    def chr_interpreter(self, word):
        init = word.find("(") + 1 
        final = word.find(")")
        if init > 0 and final > -1:
            try:
                numb = int(word[init:final])
            except ValueError:
                print("Incorrect grammar for CHR() expression at", self.counter) 

            return chr(numb)
    """
    String analyzer, converts string to regex expression. Here we dont have any CHR(), only strings
    INPUT: character dictionary *half cleansed*
    """            
    def char_to_regex(self):
        keys = self.characters.keys()
        
        for key in keys:
            val = self.characters[key] 
            separated = self.operands_identifier(val)
            sentence = self.evaluate_characters(separated)
            print("Processed CHAR", sentence)
            regex = self.to_regex(sentence, 1)
            self.characters[key] = regex
            print("Final CHAR REGEX", regex)

            

    def keyword_to_regex(self):
        keys = self.keywords.keys()

        for key in keys:
            val = self.keywords[key]
            print("Processed KEYWORDS", val)
            regex = self.to_regex(val, 2)
            print("Final KEYWORDS", regex)

            

    def operands_identifier(self, value):
        count = 0
        opMode = False
        operators = ["+", "-"]
        toBeIdentified = []
        word = ""
        string = ""
        for char in value:
            if char == '"':
                count += 1
            if count % 2 == 0 and char != "." and char not in operators and char != " ":
                word += char
            if count % 2 != 0:
                string += char

            if char in operators:
                toBeIdentified.append(char)
                if string != "" and string != '"':
                    string += '"'
                    toBeIdentified.append(string)
                
                if word != "" and word != '"':
                    toBeIdentified.append(word)
                
                word = ""
                string = ""

            
                
        if string != "" and string != '"':
                    string += '"'
                    toBeIdentified.append(string)
        if word != "" and word != '"':
            toBeIdentified.append(word)
                
        return toBeIdentified

            


            

    """
    Here we evaluate strings that contain  op + op2. We evaluate and return a string 'abc'
    INPUT: array of operands
    OUTPUT: sentence already processed
    """
    def evaluate_characters(self, array):
        operations = ["+", "-"]
        stack = []
        toBeDone = []
        sentence = ""
        for operator in array:
            if operator not in operations:
                res = self.identify_char(operator)
                res.replace('"', "")
                stack.append(res)
                
            else:   
                toBeDone.append(operator)
        
        #si es unitario, solo expulsamos lo que procesamos
        if len(toBeDone) == 0:
            return stack.pop()

        while len(toBeDone) > 0:
            second = stack.pop().strip().replace('"', "")
            first = stack.pop().strip().replace('"', "")
            op = toBeDone.pop().strip()
            sentence += first
            
            if op == "-":
                firstSet = set(first)
                secondSet = set(second)

                sentence = firstSet - secondSet
                sentence = sentence.pop()
                
            else: 
                sentence += BuilderEnum.CONCAT.value
                sentence += second
                stack.append(sentence)

        return sentence
                

    """
    Identifies if we are given a variable, it will replace that value
    x = 'ola' -> 'ola'
    """
    def identify_char(self, chars):
        keys = self.characters.keys()
        for key in keys:
            if chars == key:
                return self.characters[key]

        #si posiciones esta vacia, es un operador. 
        positions = utils.find_all_positions(chars, '"')
        if len(positions) > 0:
            if positions[0] == 0:
                positions[0] = 1
            chars = chars[positions[0]:positions[-1]]
            #return self.to_regex(chars, 1)
            return chars
        else:
            return chars

    """
    Deletes .  and the " 
    """
    def clean_char(self, toClean):
        return toClean.replace('"', "")[:-1]

    """
    Given a string like abc -> (a|b|c)
    """
    def to_regex(self, string, case):
        if case == 1:
            sentence = ""
            notToAdd = [")", "(", BuilderEnum.OR.value, "."]
            for i in range(len(string) - 1):
                sentence += string[i]
                if string[i+1] not in notToAdd and string[i] not in notToAdd:
                    
                    sentence += BuilderEnum.OR.value
                    
            
            sentence += string[-1]

        elif case == 2:
            sentence = ""
            for i in range(len(string)):
                sentence += string[i]
                #no agrega ni al ultimo ni al primer valor
                if i != 0 and len(string) - i > 2:
                    sentence += BuilderEnum.CONCAT.value
                    
                

        return sentence
        
    
    def get_tokens(self):
        line = ""
        while True:
            buffer = self.read()
            if buffer == "PRODUCTIONS":
                self.counter -= 11
                break
            line += buffer

            if line[-1] == "." and "=" in line:
                sentence = line.split("=")
                self.tokens[sentence[0]] = sentence[1]
                line = ""
            else:
                print("Grammar TOKENS error nearby char: ", self.counter)
                break


    def end(self):
        end = self.read()
        if end == self.compilerName:
            return True
        else:
            return False
    

    def __repr__(self):
        return f'<ATG chars: {self.characters} >'