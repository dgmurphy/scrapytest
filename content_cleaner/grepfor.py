import json 
  
PHRASE = 'santiago'

# Opening JSON file 
filename = '../data/ec-sentences.txt'
  
print("reading file.")

with open(filename) as f:
    lines = f.readlines()

atline = 0
sentlist = []

for line in lines:
    if PHRASE in line.lower():
        sentlist.append(line)

    if (atline % 1000) == 0:
        print("at line: " + str(atline))

    atline = atline + 1

print("Read all lines.")
print("writing " + str(len(sentlist)) + " sentences to file.")

with open("../data/ec-has-phrase.txt",'w') as fh:
    for s in sentlist:
        fh.write(s + "\n")

print("Done")
