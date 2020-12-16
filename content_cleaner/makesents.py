import spacy
import os
import shutil
import sys
import glob


def process_doc(nlp, doctext):

    SENT_MIN_LEN = 20

    doc = nlp(doctext)

    print("Building sentence list...")
    sentences = list(doc.sents)
    
    print("Sentence count: " + str(len(sentences)))

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

    print("Sentences dropped: " + str(sents_dropped))
    print("Sentences written: " + str(sents_written))

    return sentence_text_list, sents_dropped


def main():

    workdir = os.getcwd()
    print("Working dir " + workdir)

    INPUT_DIR = workdir + "/data/docs/"
    OUTPUT_DIR = workdir + "/data/sents/"

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
    files = glob.glob(INPUT_DIR + "*.txt")
    if len(files) > 0:
        print("Input file count: " + str(len(files)))
        print("Loading spacy small english model...")
        nlp = spacy.load("en_core_web_sm")
    else:
        print("No input files")
        sys.exit()

    files_processed = 0
    for fname in files:
        with open(fname, "r") as f:
            text = f.read()
            print("Processing file " + fname)
            sents, dropped = process_doc(nlp, text) # make the sents
            total_sents_dropped += dropped
            total_sents_written += len(sents)

            outname = fname.replace(INPUT_DIR, OUTPUT_DIR)
            outname = outname[:outname.index(".txt")]
            outname += "_sents.txt"
            with open(outname, "w") as outf:
                print("writing " + outname)
                outf.writelines(sents)
                files_processed += 1
                
                print("Sentence files written: " + str(files_processed))
                print("Total sents dropped: " + str(total_sents_dropped))
                print("Total sents written: " + str(total_sents_written))


    print("Sentence files written: " + str(files_processed))
    print("Total sents dropped: " + str(total_sents_dropped))
    print("Total sents written: " + str(total_sents_written))
    

if __name__ == '__main__':
    main()
    print("DONE\n")
