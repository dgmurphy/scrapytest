import json
import os
import spacy
import neuralcoref
import sys

def write_batch(filepath, jsbatch):
    with open(filepath, "a", encoding='utf8') as f:
        for jsl in jsbatch:
            f.write(json.dumps(jsl, ensure_ascii=False) + "\n")

def resolve_corefs(nlp, doc):
    
    resolved = nlp(doc)
    #print("Coref clusters: " + str(resolved._.coref_clusters))
    return resolved._.coref_resolved


# Read the input file list, process one file, then take the processed file off the list
# If the program dies before the file is processed, a restart should pick up
# where it left off.
def main():

    workdir = os.getcwd()
    print("Working dir " + workdir)

    DATA_DIR = workdir + "/data/"
    INPUT_DIR = DATA_DIR + "pe-split/"
    OUTPUT_DIR = DATA_DIR + "pe-resolved/"
    FILE_LIST = DATA_DIR + "pe_filelist.txt"

    # clean up the input_file list
    clean_files = []
    with open(FILE_LIST, "r") as f:
        infiles = f.readlines()
        for item in infiles:
            clean = item.strip()
            if len(clean) > 0:
                clean_files.append(clean + "\n")
   
    # write the clean list
    with open(FILE_LIST, "w") as f:
        f.writelines(clean_files)  
    
    print("Loading spaCy model...")
    nlp = spacy.load("en_core_web_sm")
    # Add neural coref to SpaCy's pipe
    neuralcoref.add_to_pipe(nlp)

    queue_empty = False
    files_processed = 0
    while not queue_empty:

        with open(FILE_LIST, "r") as f:
            infiles = f.readlines()
            print("Found " + str(len(infiles)) + " input files.")
        
        if len(infiles) == 0:
            queue_empty = True
            print("Finished reading input files")
        else:
            fname = infiles[0].strip()  # grab the first filename
            input_path = (INPUT_DIR + fname).strip()
            output_path = (OUTPUT_DIR + fname).strip() + ".json"
            jsbatch = []
            
            with open(input_path, "r") as f:

                lines_processed = 0
                for line in f:
                    js = json.loads(line)
                    js["resolved"] = resolve_corefs(nlp, js["doc"])
                    jsbatch.append(js)
                    lines_processed += 1
                    print(str(lines_processed) + " lines processed")
                
            write_batch(output_path, jsbatch)
            files_processed += 1
            print("files processed: " + str(files_processed))

            # update the input file list
            del infiles[0]
            with open(FILE_LIST, "w") as f:
                for item in infiles:
                    f.write(item)

    
if __name__ == '__main__':
    main()
    print("DONE\n")