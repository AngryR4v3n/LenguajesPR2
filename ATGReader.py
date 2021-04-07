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
        tmp = ""
        quoteCounter = 0
        while self.counter < len(self.words):
            """
            If we are inside " we will have an odd number
            """ 
            if self.words[self.counter] == '"':
                quoteCounter += 1
                
            """
            If the current char is " " or  "\n" and we already had a word, and we want to skip the rest... 
            """
            elif (self.words[self.counter] == " " or self.words[self.counter] == "\n") and len(tmp) > 0 and skip:
                break
            """
            If the current char is " " or "\n", we just ignore it.
            """
            elif(self.words[self.counter] == " " or self.words[self.counter] == "\n"):
                pass
            """
            If we dont want to skip the word we already have and we find a "."
            """
            elif not skip and self.words[self.counter] == ".":
                """
                If are at the end of the quotation eg: "hola". We found an end
                """
                if quoteCounter % 2 == 0:
                    tmp += self.words[self.counter]
                    break
                """
                If not we just add 
                """
                else: 
                    tmp += self.words[self.counter]
                    
            else:
                """
                Lets add! 
                """
                tmp += self.words[self.counter]
            self.counter += 1
        return tmp

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
    def compiler_name(self):
        self.compilerName = self.read()


    """
    Gets the terminals from the ATG, and modifies character obj property.
    PARAMS:
        self-> the class.
    """
    def get_characters(self):
        line = ""
        while True: 
            buffer = self.read(skip=False)

            if buffer == "KEYWORDS":
                self.counter -= 8
                break
            line += buffer
            
            #grammar checking
            if line[-1] == "." and line[-2] != "." and "=" in line:
                sentence = line.split("=") # 0 is left hand, 1 is right hand. Relative to = char
                self.characters[sentence[0]] = sentence[1]
                line =  ""
            else:
                print("Grammar CHARS error nearby char: ", self.counter)
                break

    
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