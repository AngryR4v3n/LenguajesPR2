import sys  
import os
#import dentro de la carpeta parsers
sys.path.append(os.path.abspath(os.path.join("parsers")))

from AFD import AFD
from Thompson import Thompson
from PowerSetConstruction import PowerSet
from BuilderEnum import BuilderEnum
import copy
class Parser:
    """
    Factory model for the parser, calls get_parser which decides which method to be called
    """

    def __init__(self):
        self.enums = BuilderEnum

    def parse(self, tokenArr, format, paint):
        
        if not self.isCorrect(tokenArr):
            print("Error: wrong input syntax!")
            print("Parenthesis mismatch!")
            return -1
        else:
            parser = get_parser(format)

            if format == "Thompson":

                automata = parser(tokenArr, paint)
                
                #automata.build_automata()

            if format == "PowerSet":
                thompson = Thompson()
                au = thompson.thompson_export(tokenArr)
                automata = parser(au, paint)
                

            if format == "AFD":
                automata = parser(tokenArr, paint)
                #return powerSet.build_automata()
            
            return automata

    def isCorrect(self, tkk):
        #here we check if usage of parens is correct.
        left_count = 0
        right_count = 0
        for i in range(len(tkk)):
            #esto inicia si encontramos un left parens, deberiamos antes de chequear si hay mismo num
            #de ( y ).
            
            if tkk[i].get_type() == self.enums.LEFT_PARENS.value:
                left_count +=1
                arrTkk = copy.copy(tkk)
                counter = 0 
                #we pop first elem
                token = arrTkk.pop(0)
                
                while token.get_type() != self.enums.RIGHT_PARENS.value:
                    try:
                        token = arrTkk.pop(0)
                    except IndexError:
                        return False
                                
                    counter += 1
                #chequeamos si counter es mayor a 0, si pasa aqui es porque encontro un parens derecho
                #pero deberiamos chequear este caso ()
                if(counter<=0):
                    return False
            
            elif tkk[i].get_type() == self.enums.RIGHT_PARENS.value:
                right_count += 1
        
        if (right_count == left_count):
            return True
        else:
            return False
"""
receives format or method for interpreting(.) the RegEx
"""
def get_parser(format):
    if format == "AFD":
        afd = AFD()
        return afd.afd_parser
    elif format == "Thompson":
        thompson = Thompson()
        return thompson.thompson_parser

    elif format == "PowerSet":
        Power = PowerSet()
        return Power.subset_parser

        
    else:
        raise ValueError(format)    


