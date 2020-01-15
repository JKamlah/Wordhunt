#!/usr/bin/env python3
import pdfminer.high_level
import subprocess
from pathlib import Path
from collections import defaultdict
import regex
import argparse

# Command line arguments.
arg_parser = argparse.ArgumentParser(description='Fuzzy word hunt in pdf files.')
arg_parser.add_argument("pattern", type=str, help="file or folder path")
arg_parser.add_argument("fpath", type=lambda x: Path(x), help="file or folder path", nargs='*')
arg_parser.add_argument("-e", "--error", help="Maximum of possible character error", type=int, default=1)
arg_parser.add_argument("-o", "--open", help="opens the first x pdfs in firefox (if installed)", type=int,default=0)
arg_parser.add_argument("-v", "--verbose", help="shows information, like glyphe subsitutions", type=str, default="all",choices=["all","single","list"])

args = arg_parser.parse_args()

def wordhunt(args):
    if len(args.fpath) == 1 and not args.fpath[0].is_file():
        args.fpath= list(Path(args.fpath[0]).rglob("*.pdf"))
    jsonres = defaultdict(list)
    for fname in sorted(args.fpath):
        text = pdfminer.high_level.extract_text(fname)
        for idx, line in enumerate(text.splitlines()):
            for res in regex.finditer(f"({args.pattern}){{e<={args.error}}}", line):
                if args.verbose in ["all","single"]:
                    print(f"File:   {fname}\n"
                          f"Line:   {idx}\n"
                          f"Text:   {line[:res.span()[0]]+'>>'+line[res.span()[0]:res.span()[1]]+'<<'+line[res.span()[1]:]}\n"
                          f"------------{'-'*len(line)}")
                jsonres[str(fname)].append({"Line":idx,"Text":line[:res.span()[0]]+'>>'+line[res.span()[0]:res.span()[1]]+'<<'+line[res.span()[1]:]})
    if jsonres and args.verbose in ["all","list"] or args.open != 0:
        print(f"List of all PDFs with findings:")
        for idx, key in enumerate(jsonres):
            print(key)
            if idx <= args.open-1:
                open_pdf(key)
    return jsonres

def open_pdf(fname):
    pipe = subprocess.Popen([f'firefox "{fname}"'], shell=True,stderr=subprocess.PIPE)
    return pipe

if __name__ == "__main__":
    wordhunt(args)




