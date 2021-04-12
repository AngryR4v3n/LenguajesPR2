from ATGReader import ATGReader
words = open('./C.atg', "r").read().split("\n")
reader = ATGReader(words)

print(reader.build_atg())

