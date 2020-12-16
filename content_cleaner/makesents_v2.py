# read the resolved doc content and create list of resolved 
# sentences in one large output file.

import spacy
import os
import shutil
import sys
import glob
import json


def process_doc(nlp, doctext):

    SENT_MIN_LEN = 20

    doc = nlp(doctext)
    sentences = list(doc.sents)

    sents_written = 0
    sents_dropped = 0
    sentence_text_list = []

    for s in sentences:
        text = s.text.strip()
        if len(text) > SENT_MIN_LEN:
            sentence_text_list.append(text + "\n")
            sents_written += 1
        else:
            sents_dropped += 1

    return sentence_text_list, sents_dropped


def main():

    workdir = os.getcwd()
    print("Working dir " + workdir)

    INPUT_DIR = workdir + "/data/pe-resolved/"
    OUTPUT_DIR = workdir + "/data/resolved-sents/"
    OUTFILE_NAME = OUTPUT_DIR + "pe-resolved-sents-all.txt"

    total_sents_written = 0
    total_sents_dropped = 0

    # clear the output
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    
    try:
        os.makedirs(OUTPUT_DIR)
    except:
        print("Could not make docs dir. Exiting.")
        sys.exit()
    
    # read the list of input files
    nlp = None
    files = glob.glob(INPUT_DIR + "*.json")
    if len(files) > 0:
        print("Input file count: " + str(len(files)))
        print("Loading spacy small english model...")
        nlp = spacy.load("en_core_web_sm")
    else:
        print("No input files")
        sys.exit()

    # open the output file
    with open(OUTFILE_NAME, "w") as outf:

        for fname in files:
            print("Processing file " + fname)

            with open(fname, "r") as f:
                file_sents = []
                lines_read = 0
                jslines = f.readlines()
                for jsline in jslines:
                    js = json.loads(jsline)
                    para = js["resolved"]
                    sents, dropped = process_doc(nlp, para) # make the sents
                    file_sents.extend(sents)
                    total_sents_dropped += dropped
                    total_sents_written += len(sents)
                    lines_read += 1

                    if lines_read % 10 == 0:
                        print("lines read:\t" + str(lines_read) + " \t" + 
                            " sents:\t" + str(total_sents_written))

                outf.writelines(file_sents)
                files_processed += 1
                
                print("Input files processed: " + str(files_processed))
                print("Total sents dropped: " + str(total_sents_dropped))
                print("Total sents written: " + str(total_sents_written))

    

if __name__ == '__main__':
    main()
    print("DONE\n")
