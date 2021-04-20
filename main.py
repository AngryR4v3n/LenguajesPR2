from ATGReader import ATGReader
from ATGParser import ATGParser

words = open('./C.atg', "r").read().split("\n")
reader = ATGReader(words)

reader.build_atg()

#Conversion process
atgAutomatas = ATGParser(reader)
atgAutomatas.convert_characters()
atgAutomatas.convert_keywords()
atgAutomatas.convert_tokens()
#atgAutomatas.test()

print("End parsing ATG")

