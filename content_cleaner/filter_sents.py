# read the resolved doc content and create list of resolved 
# sentences in one large output file.

import os
import shutil
import sys
import glob

def has_number(line):
    return any(char.isdigit() for char in line)

def keep(keywords, line):

    lcline = line.lower()    # convert to lower case
    for word in keywords:
        lcword =  word.lower()
        if lcword in lcline:
            return True
        elif has_number(lcline):
            return True
        else:
            return False

def main():

    workdir = os.getcwd()
    print("Working dir " + workdir)

    INPUT_DIR = workdir + "/data/resolved-sents/split/"
    OUTPUT_DIR = workdir + "/data/resolved-sents-filtered/"
    OUTFILE_NAME = OUTPUT_DIR + "pe-resolved-sents-filtered.txt"
    KEYWORDS_FILE = workdir +"/data/keywords.txt"

    total_sents_kept = 0
    total_sents_dropped = 0
    files_processed = 0

    # open the keywords file
    keywords = []
    try:
        with open(KEYWORDS_FILE, "r") as f:
            keywords = f.readlines()
    except Exception as e:
        print("Error reading keywords." + str(e))
        sys.exit()

    print("Keywords length: " + str(len(keywords)))

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
    with open(OUTFILE_NAME, "w") as outf:

        for fname in files:
            print("Processing file " + fname)

            with open(fname, "r") as f:
                keep_sents = []
                lines_read = 0
                lines = f.readlines()
                for line in lines:

                    lines_read += 1

                    if keep(keywords, line):
                        total_sents_kept += 1
                        keep_sents.append(line)
                    else:
                        total_sents_dropped += 1

                    if lines_read % 1000 == 0:
                        print("lines read:\t" + str(lines_read))

                outf.writelines(keep_sents)
                files_processed += 1
                
                print("Input files processed: " + str(files_processed))
                print("Total sents dropped: " + str(total_sents_dropped))
                print("Total sents written: " + str(total_sents_kept))

    

if __name__ == '__main__':
    main()
    print("DONE\n")
