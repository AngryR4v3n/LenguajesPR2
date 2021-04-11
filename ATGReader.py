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


    def read(self, skip=True):
       for line in self.words:
            individual = line.split()
            if len(individual) > 0:
                if individual[0] == "COMPILER":
                #execute compiler name module
                    self.compiler_name(self.words[self.counter])

                elif individual[0] == "CHARACTERS":
                    self.get_characters()
                
                elif individual[0] == "TOKENS":
                    self.get_tokens(self.words[self.counter])

                #probably a comment or sth else ...


            self.counter += 1 

    """
    Builds and gets properties of the ATG. e.g: compiler, characters...
    PARAMS: 
        self -> the class
    """
    def build_atg(self):
        while True:
            tmp = self.read()
            if tmp == "COMPILER":
                self.compiler_name()
            elif tmp == "CHARACTERS":
                self.get_characters()
            elif tmp == "KEYWORDS":
                self.get_keywords()
            elif tmp == "TOKENS":
                self.get_tokens()
            elif tmp == "PRODUCTIONS":
                self.productions()
            elif tmp == "END":
                self.end()
                break

    
    
    """
    Gets the compiler name from the ATG file, and modifies compilerName property.
    PARAMS: 
        self -> the class.
    """
    def compiler_name(self, line):
        self.compilerName = line.split()[1]


    """
    Gets the terminals from the ATG, and modifies character obj property.
    PARAMS:
        self-> the class.
    """
    def get_characters(self):
    
        #revisamos donde estamos
        currentLine = self.words[self.counter]
        #mientras no lleguemos a seccion de tokens...
        while self.counter < len(self.words):
            self.counter += 1

            #limpiamos de caracteres vacios al inicio o final
            currentLine = self.words[self.counter].strip()

            if len(currentLine) > 0:
                
            
                if currentLine.split()[0] == "TOKENS":
                    break
                
                #revisamos que todo nice en gramatica, que exista un igual y que el final sea un . 
                if "=" in currentLine and currentLine[-1] == ".": 
                    split = currentLine.split("=")
                    
                    #removemos espacios... 
                    cleanSplit = []
                    for word in split:
                        cleanSplit.append(word.strip())

                    #agregamos    
                    self.characters[cleanSplit[0]] = cleanSplit[1]
                else:
                    print("Grammar CHARS error in line: ", self.counter)
                    break

        print("Finished CHARACTERS: Syntax is correct up to here :)")
        #here we should call function that finishes to clean up stuff like "hola": '"asdad" .'
        self.char_to_regex()


    def char_to_regex(self):
        keys = self.characters.keys()
        new_chars = {}
        for key in keys:
            val = self.characters[key]
            

            
            arr_val = val.split(" ")
            #es un compuesto
            if len(arr_val) > 1:
                sentence = ""
                for operator in arr_val:
                    res = self.identify_char(operator)
                    if res:
                        sentence += res
                    else:
                        sentence += operator

                print("complex operator", sentence)
                self.characters[key] = sentence

            #es un simple
            else:
            #cleaning process & convertion 

                
                val = self.clean_char(val)
                self.characters[key]=self.to_regex(val, 1)

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
            return self.to_regex(chars, 1)
        else:
            return chars

        
    def clean_char(self, toClean):
        return toClean.replace('"', "")[:-1]


    def to_regex(self, string, case):
        if case == 1:
            sentence = ""
            for char in string:
                sentence += char
                sentence += BuilderEnum.OR.value

            return "("+sentence[:-1]+")"
                
        



        
    def get_keywords(self):
        line = ""
        while True:
            buffer = self.read()
            if buffer == "TOKENS":
                self.counter -= 6
                break
            line += buffer

            #grammar checking
            if line[-1] == "." and "=" in line:
                sentence = line.split("=")
                self.keywords[sentence[0]] = sentence[1]
                line = ""
            else:
                print("Grammar KEY error nearby char: ", self.counter)
                break

    
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