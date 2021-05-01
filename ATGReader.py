import utils
import sys  
import os
import re 
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
        self.tokens = {}
        self.compilerName = ""
        self.counter = 0
        self.ignore = []
    """
    Gets called to start analyzing the ATG file, reads line per line checking first word of each line
    """
    def build_atg(self):
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

                    self.get_characters("TOKENS", "PRODUCTIONS")
                    

                #probably a comment or sth else ...


            self.counter += 1 
    
    def get_ignore(self, line):
        spl = line.split("IGNORE SET")
        mySet = spl[1].strip()
        mySet = utils.identify_char(mySet, self.characters, False)
        mySet=mySet.replace(BuilderEnum.OR.value, "")
        mySet=mySet.replace("(", "")
        mySet=mySet.replace(")","")
        mySet=list(mySet)
        print("mySet", mySet)
        self.ignore = mySet

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
        toClean = self.compilerName
        elapsed_cycles = self.counter
        #revisamos donde estamos
        currentLine = self.words[elapsed_cycles]
        #mientras no lleguemos a seccion de tokens...
        while elapsed_cycles < len(self.words):
            
            
            elapsed_cycles += 1
            #limpiamos de caracteres vacios al inicio o final
            currentLine = self.words[elapsed_cycles].strip()

            if len(currentLine) > 0:
                
                
                    #chequeamos estructura gramatical y posibles operadores
                    
                result = self.grammar_and_op_check(currentLine)
                if currentLine.find("IGNORE SET") > -1:
                    self.get_ignore(currentLine)
                    continue
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
            self.tokens_to_regex(toClean)
            
        elif parsing == "KEYWORDS":
            self.keyword_to_regex()

    
    def grammar_and_op_check(self, currentLine):
        #revisamos que todo nice en gramatica, que exista un igual y que el final sea un . 
        if "=" in currentLine and currentLine[-1] == "." and currentLine != "": 
            split = currentLine.split("=")
            
            #removemos espacios... 
            cleanSplit = []
            for word in split:
                cleanSplit.append(word.strip())

            #chequeamos que si es CHAR(), lo pasamos de una..
            
            """
            if cleanSplit[1].find("EXCEPT KEYWORDS") > -1:
            """
            
            
            if cleanSplit[1].find("ANY") > -1:
                string = '"'
                for i in range(33, 45):
                    if i == 43 or i == 45:
                        continue
                    if i != 34:
                        string += chr(i)
                string += '"'
                cleanSplit[1] = cleanSplit[1].replace("ANY", string)

            
            #Eliminamos string literals de un quote
            cleanSplit[1] = self.change_str_literal(cleanSplit[1])


            if cleanSplit[1][-1] == ".":
                cleanSplit[1] = cleanSplit[1][0:-1]

        else:
            return None

        return cleanSplit

    def change_str_literal(self, word):
        substring = "'(([\s\S])+)'"
        x = re.findall(substring, word)
        if len(x) > 0:
            word = word.replace("'", '"')
            return word
        else:
            return word


            

    
    """
    String analyzer, converts string to regex expression. Here we dont have any CHR(), only strings
    INPUT: character dictionary *half cleansed*
    """            
    def char_to_regex(self):
        keys = self.characters.keys()
        
        for key in keys:
            val = self.characters[key]
            # number + A ->  number + A -> [+, 012345668, A]
            separated = utils.operands_identifier(val.strip())
            sentence = utils.evaluate_characters(separated, self.characters, False)
            print("Processed CHAR", sentence)
            
            regex = utils.to_regex(sentence, 1)
            regex = regex.replace('"', "")
            
            self.characters[key] = "(" + regex + ")"
            print("Final CHAR", regex)

            

    def keyword_to_regex(self):
        keys = self.keywords.keys()

        for key in keys:
            val = self.keywords[key]
            print("Processed KEYWORD", val)
            regex = utils.to_regex(val, 2).replace('"', "")
            self.keywords[key] = regex
            print("Final KEYWORD", regex)

    def tokens_to_regex(self, toClean):
        keys = self.tokens.keys()
        isExcept = False
        for key in keys:
            val = self.tokens[key]
            print("Processed TOKENS", val)
            #complejos {} [a{b{c}}] a|b[c]
            reduced = utils.complex_operators_eval(val)

            while reduced.find("}") > -1 or reduced.find("]") > -1:
                reduced = utils.complex_operators_eval(reduced)
            #simples |
            translated = utils.simple_operators(reduced)
            #identificar variables (letters)*|(digits)*
            identified, isExcept = utils.identifier(translated, self.characters)
            clean = utils.cleaner(identified, key, toClean)
            

            
            #sentence = utils.evaluate_characters(separated, self.characters, True)
            print("Final TOKEN ", clean)
            self.tokens[key] = {"token":clean, "isExcept": isExcept}
            #regex = self.to_regex(val, 3)

    
  


    def end(self):
        end = self.read()
        if end == self.compilerName:
            return True
        else:
            return False
    

    def __repr__(self):
        return f'<ATG chars: {self.characters} >'