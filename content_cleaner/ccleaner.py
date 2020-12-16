import json

def build_doc(paragraphs):
    doc = ""
    for p in paragraphs:
        p = p.strip()
        p = p.replace('\n', ' ').replace('\r', '')  #remove newlines
        doc += p + " "
    
    return doc

def main():

    DATA_DIR = "data/"
    INPUT_PATH = DATA_DIR + "power-eng.jl"
    #INPUT_PATH = DATA_DIR + "test.jl"
    OUTPUT_PATH = DATA_DIR + "power-eng-content.json"

    idx = 0
    no_content_count = 0
    content_list = []
    with open(INPUT_PATH, "r") as f:
        for line in f:

            js = json.loads(line)
            if len(js["paragraphs"]) == 0:
                no_content_count += 1
            else:
                content_list.append(js)

            idx += 1
            if idx % 10000 == 0:
                print("read line " + str(idx))
             
    print("No content count: " + str(no_content_count))
    print("Writing output file... " + OUTPUT_PATH)

    with open(OUTPUT_PATH, "w", encoding='utf8') as f:
        idx = 0
        for item in content_list:
            src_and_doc = { 
                "src": item["src_url"], 
                "doc":build_doc(item["paragraphs"])
                }
            f.write(json.dumps(src_and_doc, ensure_ascii=False) + "\n")
            idx += 1
            if idx % 10000 == 0:
                print("Lines processed " + str(idx))

if __name__ == '__main__':
    main()
    print("DONE\n")