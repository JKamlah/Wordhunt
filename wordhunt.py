#!/usr/bin/env python3
import argparse
import subprocess
from collections import defaultdict
from pathlib import Path

#import pdfminer.high_level (activate if you only want to search pdfs and you do not like textract)
import textract
import regex

# Command line arguments
arg_parser = argparse.ArgumentParser(description='Fuzzy word hunt in pdf files.')
arg_parser.add_argument("pattern", type=str, help="Pattern of character as search term")
arg_parser.add_argument("fpath", type=lambda x: Path(x), help="File or folder path", nargs='*')
arg_parser.add_argument("-e", "--error", help="Maxium number of character errors", type=int, default=1)
arg_parser.add_argument("-x", "--extension", help="Fileextension", type=str, default=".pdf")
arg_parser.add_argument("-o", "--open", help="Opens the first x pdfs in firefox (if installed)", type=int, default=0)
arg_parser.add_argument("-v", "--verbose", help="Shows information, like glyphe subsitutions", type=str, default="all",
                        choices=["all", "single", "list"])

args = arg_parser.parse_args()


def print_finding(res, fname, idx, line):
    print(f"File:   {fname}\n"
          f"Line:   {idx}\n"
          f"Text:   {line[:res.span()[0]] + '>>' + line[res.span()[0]:res.span()[1]] + '<<' + line[res.span()[1]:]}\n"
          f"------------{'-' * len(line) if len(line) < 60 else 60}")
    return


def wordhunt(args):
    if len(args.fpath) == 1 and not args.fpath[0].is_file():
        args.fpath = list(Path(args.fpath[0]).rglob(f"*{args.ext}"))
    jsonres = defaultdict(list)
    for fname in sorted(args.fpath):
        text = textract.process(str(fname)).decode("utf-8")
        #text = pdfminer.high_level.extract_text(fname) alternative without textract for pdf files
        for idx, line in enumerate(text.splitlines()):
            for res in regex.finditer(f"({args.pattern}){{e<={args.error}}}", line):
                if args.verbose in ["all", "single"]:
                    print_finding(res, fname, idx, line)
                jsonres[str(fname)].append({"Line": idx, "Text": line[:res.span()[0]] + '>>' + line[
                                                                                               res.span()[0]:res.span()[
                                                                                                   1]] + '<<' + line[
                                                                                                                res.span()[
                                                                                                                    1]:]})
    if jsonres and args.verbose in ["all", "list"] or args.open != 0:
        print(f"List of all pattern containing files:")
        for idx, key in enumerate(jsonres):
            print(key)
            if idx <= args.open - 1:
                open_file(key, args)
    return jsonres


def open_file(fname, args):
    pipe = None
    if args.ext == ".pdf":
        pipe = subprocess.Popen([f'firefox "{fname}"'], shell=True, stderr=subprocess.PIPE)
    return pipe


if __name__ == "__main__":
    wordhunt(args)