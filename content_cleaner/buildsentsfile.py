import os
import shutil
import sys
import glob

def process_doc(nlp, line):

    doc = nlp(line)
    # do some processing of the line here

    return 

def main():

    workdir = os.getcwd()
    print("Working dir " + workdir)

    INPUT_DIR = workdir + "/data/sents/"
    OUTPUT_DIR = workdir + "/data/filtered-sents/"
    OUTPUT_FILE = OUTPUT_DIR + "power-eng-all-sentences.txt"


    # clear the output
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    
    try:
        os.makedirs(OUTPUT_DIR)
    except:
        print("Could not make docs dir. Exiting.")
        sys.exit()
    
    # read the list of input files
    #nlp = None
    files = glob.glob(INPUT_DIR + "*.txt")
    if len(files) > 0:
        print("Input file count: " + str(len(files)))
    else:
        print("No input files")
        sys.exit()

    files_processed = 0
    for fname in files:
        with open(fname, "r") as f:
            text = f.read()
            #print("Processing file " + fname)
            #sents, dropped = process_doc(nlp, text) # make the sents

            with open(OUTPUT_FILE, "a") as outf:
                print("appending " + fname)
                outf.write(text)
                files_processed += 1
                
                print("Sentence files processed: " + str(files_processed))
   

if __name__ == '__main__':
    main()
    print("DONE\n")
