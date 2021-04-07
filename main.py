from ATGReader import ATGReader

words = open('./C.atg', "r").read()
reader = ATGReader(words)

print(reader.build_atg())

