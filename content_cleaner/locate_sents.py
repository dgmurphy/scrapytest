# run sentences through mordecai 

import os
import shutil
import sys
import glob
import json
import requests
from datetime import datetime


def update_ccount(ccode, ccount):

    if ccode in ccount:
        ccount[ccode] += 1
    else:
        ccount[ccode] = 1

    return ccount


# header "Content-Type: application/json" 
# request POST 
# data '{"text":"I traveled from Paris to Ottawa."}'
# http://localhost:5000/places
#
def locate(sentence):
    
    try:
        url = 'http://localhost:5000/places'
        sent = {"text":sentence}
        resp = requests.post(url, json = sent, timeout=30.0)
        places = resp.json()
        place = None

        # TODO mordapi retuns a list when no place was found
        #  but returns an object when found. Needs to return
        #  same type

        if type(places) is list:
            place = places[0]
        else:
            place = places
        
        if place["placename"] == "NA":
            return None
        else:
            place["sentence"] = sentence
            return place

    except Exception as exception:

        print("Exception" + str(exception))
        return None
 

def main():

    workdir = os.getcwd()
    print("Working dir " + workdir)

    INPUT_DIR = workdir + "/data/resolved-sents-filtered/split/"
    OUTPUT_DIR = workdir + "/data/resolved-sents-located/"
    OUTFILE_NAME_HASLATLONG = OUTPUT_DIR + "pe-resolved-sents-filtered-latlong.txt"
    OUTFILE_NAME_NOLATLONG = OUTPUT_DIR + "pe-resolved-sents-filtered-nolatlong.txt"

    lines_read = 0
    total_sents_kept = 0
    total_withlatlong = 0
    total_nolatlong = 0
    total_sents_dropped = 0
    files_processed = 0

    country_count = {}

    # clear the output
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    
    try:
        os.makedirs(OUTPUT_DIR)
    except:
        print("Could not make docs dir. Exiting.")
        sys.exit()
    
    # read the list of input files
    files = glob.glob(INPUT_DIR + "pe-*")
    if len(files) > 0:
        print("Input file count: " + str(len(files)))
    else:
        print("No input files")
        sys.exit()

    # open the output file
    with open(OUTFILE_NAME_HASLATLONG, "w") as out_latlong, open(OUTFILE_NAME_NOLATLONG, "w") as out_nolatlong:

        for fname in files:
            print("Processing file " + fname + " " + str(datetime.now()))

            with open(fname, "r") as f:
                latlong_jsa = []   # json array
                nolatlong_jsa = []
                
                lines = f.readlines()
                for line in lines:

                    lines_read += 1

                    location_js = locate(line)
                    if location_js is not None:
                        total_sents_kept += 1
                        country_count = update_ccount(location_js["countrycode"], country_count)
                        if location_js["lat"] == "NA":
                            nolatlong_jsa.append(location_js)
                            total_nolatlong += 1
                        else:
                            latlong_jsa.append(location_js)
                            total_withlatlong += 1
                    else:
                        total_sents_dropped += 1

                    if lines_read % 1000 == 0:
                        print("lines read:\t" + str(lines_read))
                        print(json.dumps(country_count, indent=4))

    
                # write to files
                out_latlong.writelines(json.dumps(latlong_jsa, indent=4))
                out_nolatlong.writelines(json.dumps(nolatlong_jsa, indent=4))
                files_processed += 1
                
                print("Input files processed: " + str(files_processed))
                print("Total sents dropped: " + str(total_sents_dropped))
                print("Total sents written: " + str(total_sents_kept))
                print("Total with lat long: " + str(total_withlatlong))
                print("Total without lat long: " + str(total_nolatlong))
                print(json.dumps(country_count, indent=4))

    

if __name__ == '__main__':
    main()
    print("DONE\n")
