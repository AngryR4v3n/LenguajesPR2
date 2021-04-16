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
        self.tokens = {}
        self.compilerName = ""
        self.counter = 0

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
            self.tokens_to_regex()
            
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
            separated = utils.operands_identifier(val)
            sentence = utils.evaluate_characters(separated, self.characters)
            print("Processed CHAR", sentence)
            regex = utils.to_regex(sentence, 1)
            self.characters[key] = regex
            print("Final CHAR REGEX", regex)

            

    def keyword_to_regex(self):
        keys = self.keywords.keys()

        for key in keys:
            val = self.keywords[key]
            print("Processed KEYWORDS", val)
            regex = utils.to_regex(val, 2).replace('"', "")
            self.keywords[key] = regex
            print("Final KEYWORDS", regex)

    def tokens_to_regex(self):
        keys = self.tokens.keys()
        for key in keys:
            val = self.tokens[key]
            print("Processed TOKENS", val)
            separated = utils.operands_identifier_v2(val)
            sentence = utils.evaluate_characters(separated, self.characters)
            print("hmm, ", sentence)
            #regex = self.to_regex(val, 3)

    
  


    def end(self):
        end = self.read()
        if end == self.compilerName:
            return True
        else:
            return False
    

    def __repr__(self):
        return f'<ATG chars: {self.characters} >'