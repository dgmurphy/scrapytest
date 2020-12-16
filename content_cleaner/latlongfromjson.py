import json
import os

def main():

    workdir = os.getcwd()
    print("Working dir " + workdir)

    INPUT_DIR =  workdir + "/data/resolved-sents-located/"
    INPUT_FILE = INPUT_DIR + "pe-resolved-sents-filtered-latlong.txt"
    OUTPUT_FILE = INPUT_DIR + "pe-latlongs.txt"

    latlongs = []

    with open(INPUT_FILE, "r") as inf:
        places_jsa = json.load(inf)

        for place in places_jsa:
            latlong = place["lat"] + "\t" + place["lon"] + "\n"
            latlongs.append(latlong)

    with open(OUTPUT_FILE, "w") as outf:
        outf.write("latitude \t longitude \n")
        outf.writelines(latlongs)

if __name__ == '__main__':
    main()
    print("DONE\n")
