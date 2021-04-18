import tokenizer as Token
from BuilderEnum import BuilderEnum
class Builder():
    
    
    def __init__(self, instruction):
        self.instruction = iter(instruction)
        self.next_char()
        self.tokensArr =[]
        print("ALL", BuilderEnum.ALL_OPERATORS.value)
        self.operators = BuilderEnum.ALL_OPERATORS.value
        self.parens = ["(", ")"]
        self.enums = BuilderEnum
        self.counter = 0
        
        

    #(a|b)
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

            #caso 0: tenemos un string literal! 
            if(self.char == '"'):
                self.counter += 1

            
            
            #caso 1: tenemos un token de tipo simbolo
            if (self.char not in self.operators and self.char):

                
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
            elif(self.char in self.parens and self.counter % 2 == 0):
                if self.char == self.enums.LEFT_PARENS.value:
                    token = Token.Tokenizer(type_t=self.enums.LEFT_PARENS.value, value=None)
                elif self.char == self.enums.RIGHT_PARENS.value:
                    token = Token.Tokenizer(type_t=self.enums.RIGHT_PARENS.value, value=None)

            self.tokensArr.append(token)

            self.next_char()

                
    
