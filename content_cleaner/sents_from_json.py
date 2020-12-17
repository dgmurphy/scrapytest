import json 
  
# Opening JSON file 
filename = '../data/energy-central-hascontent.json'
  
print("reading file.")

with open(filename) as f:
    lines = f.readlines()

atline = 0
data = {}
sentlist = []

for line in lines:
    data = json.loads(line) 
    paras  = data['paragraphs']
    for sent in paras:
        sentlist.append(sent)

    if (atline % 1000) == 0:
        print("at line: " + str(atline))

    atline = atline + 1

print("Read all lines.")
print("writing " + str(len(sentlist)) + " sentences to file.")

with open("../data/ec-sentences.txt",'w') as fh:
    for s in sentlist:
        fh.write(s + "\n")

print("Done")
