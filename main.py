from ATGReader import ATGReader
from ATGParser import ATGParser

words = open('./C.atg', "r").read().split("\n")
reader = ATGReader(words)

reader.build_atg()

#Conversion process
atgAutomatas = ATGParser(reader)
atgAutomatas.test()


print("End reading ATG")

