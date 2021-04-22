import sys  
import os
sys.path.append(os.path.abspath(os.path.join("AFD/AFN")))
import automataGenerator
class ATGParser():
    def __init__(self, ATG):
        self.ATG = ATG
        self.characters = {}
        self.tokens = {}
        self.keywords = {}

    def convert_characters(self):
        keys = self.ATG.characters.keys()
        hashType = ""
        for key in keys:
            hashType = f"CHARACTER - {key}"
            toConvert = self.ATG.characters[key]
            automata = automataGenerator.single(toConvert, hashType)
            self.characters[key] = automata

    def convert_keywords(self):
        keys = self.ATG.keywords.keys()

        for key in keys:
            hashType = f"KEYWORD - {key}"
            toConvert = self.ATG.keywords[key]
            automata = automataGenerator.single(toConvert, hashType)
            self.keywords[key] = automata

    def convert_tokens(self):
        keys = self.ATG.tokens.keys()
        for key in keys:
            hashType = f"TOKEN - {key}"
            toConvert = self.ATG.tokens[key]
            automata = automataGenerator.single(toConvert, hashType)
            self.tokens[key] = automata



    def test(self):
        automata = automataGenerator.test()

