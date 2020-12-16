import json
import shutil
import os
import sys

workdir = os.getcwd()
print("Working dir " + workdir)

DATA_DIR = workdir + "/data/"
DOCS_DIR = DATA_DIR + "docs/"
INPUT_PATH = DATA_DIR + "power-eng-content.json"
OUTPUT_PREFIX = DOCS_DIR + "power-eng-content_page_"
DOC_SET_SIZE = 100
PAGE_LIMIT = 10000  # drops content beyind the page limit

def write_doc(doclist, pagenum):

    output_path = OUTPUT_PREFIX + str(pagenum) + ".txt"
    with open(output_path, "w", encoding="utf-8") as f:
        for doc in doclist:
            f.write(doc + "\n\n")

    print("Wrote " + output_path)


def main():

    if os.path.exists(DOCS_DIR):
        shutil.rmtree(DOCS_DIR)
    
    try:
        os.makedirs(DOCS_DIR)
    except:
        print("Could not make docs dir. Exiting.")
        sys.exit()


    lines_read = 0
    doclist = []
    with open(INPUT_PATH, "r") as f:
        for line in f:

            js = json.loads(line)
            doclist.append(js["doc"])
            lines_read += 1
            if lines_read % 10000 == 0:
                print("read line " + str(lines_read))
    
    docs_processed = 0
    pagenum = 1
    doc_page = []
    for doc in doclist:

        if pagenum > PAGE_LIMIT:
            break

        doc_page.append(doc)
        docs_processed += 1   

        if docs_processed == DOC_SET_SIZE:
            write_doc(doc_page, pagenum)  # write a set of docs
            doc_page = []
            docs_processed = 0
            pagenum += 1   

          
    if len(doc_page) > 0:
        write_doc(doc_page, pagenum)  # write the last set
            

if __name__ == '__main__':
    main()
    print("DONE\n")