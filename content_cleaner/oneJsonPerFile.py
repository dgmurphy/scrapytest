import json
import datetime

# Opening JSON file

ymd = str((datetime.datetime.now()))[0:10]

infilename = '../data/energy-central-noparagraphs.txt'
outfileprefix = '../data/jsonfiles/energy-central_' + ymd + "_page_"

print("reading file.")

with open(infilename, 'r') as inf:
    lines = inf.readlines()

print("writing " + str(len(lines)) + " files.")
outfile_idx = 0
for line in lines:

    inData = json.loads(line)

    outfile_idx += 1
    outfilename = outfileprefix + str(outfile_idx) + ".json"

    with open(outfilename, 'w') as outf:
        outf.write(json.dumps(inData))

    if (outfile_idx % 1000) == 0:
        print("wrote: " + outfilename)


print("Done")
