import json
import os
import spacy
import neuralcoref

def write_batch(filepath, jsbatch):
    with open(filepath, "a", encoding='utf8') as f:
        for jsl in jsbatch:
            f.write(json.dumps(jsl, ensure_ascii=False) + "\n")

def resolve_corefs(nlp, doc):
    
    resolved = nlp(doc)
    #print("Coref clusters: " + str(resolved._.coref_clusters))
    return resolved._.coref_resolved

def main():

    workdir = os.getcwd()
    print("Working dir " + workdir)

    DATA_DIR = workdir + "/data/"
    INPUT_PATH = DATA_DIR + "power-eng-content.json"
    OUTPUT_PATH = DATA_DIR + "power-eng-corefresolved.json"
    WRITE_BATCH = 10

    if os.path.exists(OUTPUT_PATH):
        os.remove(OUTPUT_PATH)        

    print("Loading spaCy model...")
    nlp = spacy.load("en_core_web_sm")
    # Add neural coref to SpaCy's pipe
    neuralcoref.add_to_pipe(nlp)


    idx = 0
    jsbatch = []
    with open(INPUT_PATH, "r") as f:

        for line in f:
            js = json.loads(line)
            js["resolved"] = resolve_corefs(nlp, js["doc"])
            jsbatch.append(js)
            idx += 1
            if idx % WRITE_BATCH == 0:
                write_batch(OUTPUT_PATH, jsbatch)
                jsbatch = []
                print("docs processed: " + str(idx))
             
    if len(jsbatch) > 0:
        write_batch(OUTPUT_PATH, jsbatch)
        print("docs processed: " + str(idx))

    
if __name__ == '__main__':
    main()
    print("DONE\n")