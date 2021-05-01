import tokenizer as Token
from BuilderEnum import BuilderEnum
class Builder():
    
    
    def __init__(self, instruction, dictionary=None):
        self.raw = instruction
        self.instruction = iter(instruction)
        self.next_char()
        self.tokensArr =[]
        self.operators = BuilderEnum.ALL_OPERATORS.value
        self.operators.pop(5)
        self.parens = ["(", ")"]
        self.enums = BuilderEnum
        self.counter = 0
        self.hashNumb = 0
        self.identifier = dictionary
        
        

    
    def get_identifier(self, counter):
        keys = self.identifier.keys()
        keys = list(keys)
        return keys[counter]

    
    def set_instruction(self, instruction):
        self.instruction = iter(instruction)
        self.next_char()

    def getTokenArr(self):
        return self.tokensArr

    def next_char(self):
        try:
            self.char =  next(self.instruction)

        except StopIteration:
            self.char = None

    def generator(self):
        #iteramos sobre la instruccion
        while self.char != None:
            token = None
            #caso 0: tenemos un string literal! 
            if(self.char == '"') or (self.char == "'"):
                self.counter += 1

            
            
            #caso 1: tenemos un token de tipo simbolo
            if (self.char not in self.operators and self.char and self.char != '"') or (self.counter % 2 != 0):

                if (self.counter % 2 != 0 and self.char and self.counter > 0):
                    if(self.char == self.enums.HASH.value):
                        
                        token = Token.Tokenizer(type_t=self.enums.SYMBOL.value, value=self.char, identifier=self.get_identifier(self.hashNumb))
                        self.hashNumb += 1
                    elif self.char == '"':
                        token = None
                    elif self.char in self.operators and self.char != '(' and self.char != ')':
                        if self.char == self.enums.KLEENE.value:
                            token = Token.Tokenizer(type_t=self.enums.KLEENE.value, value=None)
                        elif self.char == self.enums.PLUS.value:
                            token = Token.Tokenizer(type_t=self.enums.PLUS.value, value=None)
                        elif self.char == self.enums.OR.value:
                            token = Token.Tokenizer(type_t=self.enums.OR.value, value=None)
                        elif self.char == self.enums.CONCAT.value:
                            token = Token.Tokenizer(type_t=self.enums.CONCAT.value, value=None)

                    else:
                        #cierre de parens.
                        if self.char == "Л":
                            token = Token.Tokenizer(type_t=self.enums.SYMBOL.value, value=")")    
                        #abre parens..
                        elif self.char == "Г":
                            token = Token.Tokenizer(type_t=self.enums.SYMBOL.value, value="(")
                        
                        #comilla simple..
                        elif self.char == "Д":
                            token = Token.Tokenizer(type_t=self.enums.SYMBOL.value, value="'")
                        #comilla doble..
                        elif self.char == "Ш":
                            token = Token.Tokenizer(type_t=self.enums.SYMBOL.value, value='"')
                        else:
                            token = Token.Tokenizer(type_t=self.enums.SYMBOL.value, value=self.char)
                        
                elif (self.counter % 2 == 0 and self.char):
                    if(self.char == self.enums.HASH.value):
                        
                        token = Token.Tokenizer(type_t=self.enums.SYMBOL.value, value=self.char, identifier=self.get_identifier(self.hashNumb))
                        self.hashNumb += 1
                    
                    else:
                        #cierre de parens.
                        if self.char == "Л":
                            token = Token.Tokenizer(type_t=self.enums.SYMBOL.value, value=")")    
                        #abre parens..
                        elif self.char == "Г":
                            token = Token.Tokenizer(type_t=self.enums.SYMBOL.value, value="(")
                        
                        #comilla simple..
                        elif self.char == "Д":
                            token = Token.Tokenizer(type_t=self.enums.SYMBOL.value, value="'")
                        #comilla doble..
                        elif self.char == "Ш":
                            token = Token.Tokenizer(type_t=self.enums.SYMBOL.value, value='"')
                        else:
                            token = Token.Tokenizer(type_t=self.enums.SYMBOL.value, value=self.char)
                        



            
            #caso 2: tenemos un token de tipo operador
            elif(self.char in self.operators):
                
                if self.char == self.enums.KLEENE.value:
                    token = Token.Tokenizer(type_t=self.enums.KLEENE.value, value=None)
                elif self.char == self.enums.PLUS.value:
                    token = Token.Tokenizer(type_t=self.enums.PLUS.value, value=None)
                elif self.char == self.enums.OR.value:
                    token = Token.Tokenizer(type_t=self.enums.OR.value, value=None)
                elif self.char == self.enums.CONCAT.value:
                    token = Token.Tokenizer(type_t=self.enums.CONCAT.value, value=None)

            #caso 3: tenemos un token de tipo parens
            '''
            elif(self.char in self.parens and self.counter % 2 == 0):
                if self.char == self.enums.LEFT_PARENS.value:
                    token = Token.Tokenizer(type_t=self.enums.LEFT_PARENS.value, value=None)
                elif self.char == self.enums.RIGHT_PARENS.value:
                    token = Token.Tokenizer(type_t=self.enums.RIGHT_PARENS.value, value=None)
            '''
            
            if token:
                self.tokensArr.append(token)

            self.next_char()

                
    
