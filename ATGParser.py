import sys  
import os
sys.path.append(os.path.abspath(os.path.join("AFD/AFN")))
import automataGenerator
class ATGParser():
    def __init__(self, ATG):
        self.ATG = ATG
        self.characters = {}

    def convert_characters(self):
        keys = self.ATG.characters.keys()

        for key in keys:
            toConvert = self.ATG.characters[key]
            automata = automataGenerator.single(toConvert)
            self.characters[key] = automata

    def test(self):
        automata = automataGenerator.test()

