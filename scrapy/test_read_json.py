import json 
  
# Opening JSON file 
filename = './scrapy/energy-central.json'
  
with open(filename) as f:
    lines = f.readlines()

# returns JSON object as  
# a dictionary 
data = {}
for line in lines:
    data = json.loads(line) 
    #print(data['src_url'])

htmldata = data['html']
print(htmldata)

with open("./scrapy/out.html",'w') as fh:
     fh.write(htmldata)

