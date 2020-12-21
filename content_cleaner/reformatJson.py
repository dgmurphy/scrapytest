import json 
  
# Opening JSON file 
infilename = '../data/energy-central-hascontent.json'
outfilename = '../data/energy-central-noparagraphs.txt'
  
print("reading file.")

with open(infilename, 'r') as inf:
    lines = inf.readlines()

with open(outfilename, 'w') as outf:

    outData = {
        'documentURI': '',
        'ingestDate': '',
        'content': '',
        'ingestSource': ''
    }
 
    atline = 0

    for line in lines:
        inData = json.loads(line) 
        outData['documentURI'] = inData['src_url']
        outData['ingestDate'] = inData['ingest_date']
        outData['content'] = inData['html']
        outData['ingestSource'] = inData['spider_name']
        outstr = json.dumps(outData) + "\n"
        outf.write(outstr)

        if (atline % 1000) == 0:
            print("at line: " + str(atline))

        atline = atline + 1


print("Done")
