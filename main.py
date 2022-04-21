#! /usr/bin/python3

import sys
import os
from argparse import ArgumentParser

sys.path.append(os.path.join(os.path.dirname(__file__), ".", "utils"))
from extractor import Extractor

class Reporter(Extractor):

    def get_formatted_line(self, ln):

        unformatted_results = self.extract(ln)
        formatted_results = []
        for ur in unformatted_results:
            if ur is None:
                formatted_results.append("")
            elif ur == 888:
                formatted_results.append("NI")
            else:
                formatted_results.append(str(ur))

        return "\t".join(formatted_results)

if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("--ifile", type=str, help="file containing newline-delimited docs or snippets")
    args = parser.parse_args()

    r = Reporter()

    with open(args.ifile, "r") as f:
        for ln in f.readlines():
            print(r.get_formatted_line(ln))
