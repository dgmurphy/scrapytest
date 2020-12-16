import json
import os

def main():

    workdir = os.getcwd()
    print("Working dir " + workdir)

    INPUT_DIR =  workdir + "/data/resolved-sents-located/"
    INPUT_FILE = INPUT_DIR + "pe-resolved-sents-filtered-latlong.txt"
    OUTPUT_FILE = INPUT_DIR + "pe-fencefiltered.txt"

    MIN_LAT = -33.671
    MAX_LAT = -32.569
    MIN_LON = -72.000
    MAX_LON = -70.192

    keep_jsa = []

    with open(INPUT_FILE, "r") as inf:
        places_jsa = json.load(inf)

        for place in places_jsa:
            lat = float(place["lat"])
            lon = float(place["lon"])
            if lat > MIN_LAT and lat < MAX_LAT:
                if lon > MIN_LON and lon < MAX_LON:
                    keep_jsa.append(place)
                    print("Match: " + place["sentence"])

    with open(OUTPUT_FILE, "w") as outf:
        outf.writelines(json.dumps(keep_jsa, indent=4))

if __name__ == '__main__':
    main()
    print("DONE\n")
