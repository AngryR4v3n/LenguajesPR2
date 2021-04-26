import sys  
import os
sys.path.append(os.path.abspath(os.path.join("AFD/AFN")))
from BuilderEnum import BuilderEnum 
import automataGenerator
class ATGParser():
    def __init__(self, ATG):
        self.ATG = ATG
        self.characters = {}
        self.tokens = {}
        self.keywords = {}

    def main_tree(self):
        keys = self.ATG.characters.keys()
        all_tree = []
        hashType = ""
        for key in keys:
            hashType = f"CHARACTER - {key}"
            toConvert = self.ATG.characters[key]
            all_tree.append(toConvert)

        """
        keys = self.ATG.tokens.keys()
        for key in keys:
            toConvert = self.ATG.tokens[key]
            all_tree.append(toConvert)
        """
        """
        keys = self.ATG.keywords.keys()
        for key in keys:
            toConvert = self.ATG.keywords[key]
            all_tree.append(toConvert)
        """

        automataGenerator.whole_regex(all_tree, self.ATG.characters)




    def test(self):
        automata = automataGenerator.test()

