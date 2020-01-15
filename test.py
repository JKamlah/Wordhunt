import argparse
from pathlib import Path

from wordhunt import wordhunt, open_pdf

arg_parser = argparse.ArgumentParser(description='Fuzzy word hunt in pdf files.')
arg_parser.add_argument("pattern", type=str, help="file or folder path")
arg_parser.add_argument("fpath", type=lambda x: Path(x), help="file or folder path", nargs='*')
arg_parser.add_argument("-e", "--error", help="Maximum of possible character error", type=int, default=1)
arg_parser.add_argument("-o", "--open", help="opens the first x pdfs in firefox (if installed)", type=int, default=0)
arg_parser.add_argument("-v", "--verbose", help="shows information, like glyphe subsitutions", type=str, default="all",
                        choices=["all", "single", "list"])
args = arg_parser.parse_args()


def test():
    args.fpath = [Path("./Test/")]
    args.pattern = "Hey"
    res = wordhunt(args)
    assert res != {}, "test failed, empty result"
    for reskey in res:
        assert res[reskey][0]['Text'] == '>>Hey<<', "test failed, wrong result"


def test2():
    res = open_pdf("./Test/Test.pdf")
    assert res.stderr.readline() == b'', "test failed, maybe firefox is not installed"
