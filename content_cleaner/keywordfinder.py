import json
import os

def main():

    workdir = os.getcwd()
    print("Working dir " + workdir)

    INPUT_DIR =  workdir + "/data/resolved-sents-filtered/"
    INPUT_FILE = INPUT_DIR + "pe-resolved-sents-filtered.txt"
    OUTPUT_FILE = INPUT_DIR + "chile-keywordfiltered.txt"

    find_word = "chile"

    keep_jsa = []

    with open(INPUT_FILE, "r") as inf:
        sents = inf.readlines()

        for sent in sents:
            sent_lower = sent.lower()
            if find_word in sent_lower:
                keep_jsa.append(sent)
                print("Match: " + sent)

    with open(OUTPUT_FILE, "w") as outf:
        outf.writelines(json.dumps(keep_jsa, indent=4))

if __name__ == '__main__':
    main()
    print("DONE\n")
