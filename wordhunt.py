import pdfminer.high_level
from pathlib import Path
from collections import defaultdict
import sys
import regex

def wordhunt(fpath,pattern,error=1,verbose="all"):
    fpath = Path(fpath)
    jsonres = defaultdict(list)
    for fname in sorted(fpath.rglob("*.pdf")):
        text = pdfminer.high_level.extract_text(fname)
        for idx, line in enumerate(text.splitlines()):

            for res in regex.finditer(f"({pattern}){{e<={error}}}", line):
                if verbose in ["all","single"]:
                    print(f"File:   {fname}\n"
                        f"Line:   {idx}\n"
                        f"Text:   {line[:res.span()[0]]+'>>'+line[res.span()[0]:res.span()[1]]+'<<'+line[res.span()[1]:]}\n"
                        f"--------{'-'*len(line)}")
                jsonres[str(fname)].append({"Line":idx,"Text":line[:res.span()[0]]+'>>'+line[res.span()[0]:res.span()[1]]+'<<'+line[res.span()[1]:]})
    if verbose in ["all","list"]:
        print(f"List of all PDFs with findings:")
        for key in jsonres:
            print(key)
    return jsonres

if __name__ == "__main__":
    fpath = sys.argv[1]
    pattern = sys.argv[2]
    error = sys.argv[3] if len(sys.argv) == 4 else int(len(pattern) / 10)
    if error == 0: error = 1
    wordhunt(fpath,pattern,error)



