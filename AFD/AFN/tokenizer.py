
class Tokenizer:
    

    

    """
    Returns a token, tokens have a type (whether they are an operator or a symbol)
    and they also have a value.
    """
    def __init__(self, type_t, value=None):
        self.type = type_t
        self.value = value
        

    """
    Sets value for the token
    """
    def set_value(self,data):
        self.value = data
    """
    Gets type for token
    """
    def get_type(self):
        return self.type

    def set_type(self, tipo):
        self.type = tipo

    
            
    """
    Gets value of token
    """
    def get_value(self):
        return self.value


    """
    Print for debugging 
    """
    def __repr__(self):
        return f"<Token type: {self.type} with value: {self.value}>"