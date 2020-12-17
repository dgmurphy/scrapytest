import json 
  
# Opening JSON file 
filename = '../data/energy-central.json'
  
print("reading file.")

with open(filename) as f:
    lines = f.readlines()

atline = 0
data = {}
goodlines = []
no_text = 0
for line in lines:
    data = json.loads(line) 
    if len(data['paragraphs']) == 0:
        no_text = no_text + 1
    else:
        goodlines.append(line)

    if (atline % 1000) == 0:
        print("at line: " + str(atline))

    atline = atline + 1

print("Read all lines.")
print(str(no_text) + " with no text.")
print("writing " + str(len(goodlines)) + " good lines to file.")

with open("../data/energy-central-hascontent.json",'w') as fh:
    fh.writelines(goodlines)

print("Done")
