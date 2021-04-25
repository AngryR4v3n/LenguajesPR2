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
                    #chequeamos estructura gramatical y posibles operadores
                    
                result = self.grammar_and_op_check(currentLine)

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

    
    def grammar_and_op_check(self, currentLine):
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
                cleanSplit[1] = converted + '.'
            
            """
            if cleanSplit[1].find("EXCEPT KEYWORDS") > -1:
            """
            
            
            if cleanSplit[1].find("ANY") > -1:
                string = '"'
                for i in range(33, 45):
                    if i == 43 or i == 45:
                        continue
                    if i != 34:
                        string += repr(chr(i))
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

    def chr_interpreter(self, word):
        substring = "\d+"
        startPos = []
        endPos = []
        numbArr = []
        for m in re.finditer(substring, word):
            startPos.append(m.start())
            endPos.append(m.end())
        
        for i in range(len(startPos)):
            try:
                numbArr.append(int(word[startPos[i]:endPos[i]]))
            except ValueError:
                print("Incorrect grammar for CHR() expression at", self.counter)

        if len(numbArr) <= 1:
            try:
                numb = int(numbArr[0])
                if numb == 148:
                    numb = 32
            except ValueError:
                print("Incorrect grammar for CHR() expression at", self.counter) 

            return repr(chr(numb))

        else:
            resta = numbArr[-1] - numbArr[0]
            answer = []
            for i in range(1,resta):
                if numbArr[0] + i == 32:
                    continue
                else:
                    answer.append(numbArr[0] + i)
            stringAns = ""
            for number in answer:
                a = repr(chr(number))
                stringAns += a

            return stringAns

            

        
    """
    String analyzer, converts string to regex expression. Here we dont have any CHR(), only strings
    INPUT: character dictionary *half cleansed*
    """            
    def char_to_regex(self):
        keys = self.characters.keys()
        
        for key in keys:
            val = self.characters[key] 
            separated = utils.operands_identifier(val)
            sentence = utils.evaluate_characters(separated, self.characters, False)
            print("Processed CHAR", sentence)
            
            if sentence.find("\\") > -1:
                sentence = sentence[2:]
                regex = utils.to_regex(sentence, 2)
            else:
                regex = utils.to_regex(sentence, 1)
            self.characters[key] = regex
            print("Final CHAR", regex)

            

    def keyword_to_regex(self):
        keys = self.keywords.keys()

        for key in keys:
            val = self.keywords[key]
            print("Processed KEYWORD", val)
            regex = utils.to_regex(val, 2).replace('"', "")
            self.keywords[key] = regex
            print("Final KEYWORD", regex)

    def tokens_to_regex(self):
        keys = self.tokens.keys()
        for key in keys:
            val = self.tokens[key]
            print("Processed TOKENS", val)
            separated = utils.operands_identifier_v2(val)
            sentence = utils.evaluate_characters(separated, self.characters, True)
            print("Final TOKEN ", sentence)
            self.tokens[key] = sentence
            #regex = self.to_regex(val, 3)

    
  


    def end(self):
        end = self.read()
        if end == self.compilerName:
            return True
        else:
            return False
    

    def __repr__(self):
        return f'<ATG chars: {self.characters} >'