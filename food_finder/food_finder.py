#!/usr/bin/env python2

"""Main entry-point for the iRobot Interview Project ("food finder").

Author: Alex Richard Ford (arf4188@gmail.com)
"""

import colorlog
import argparse

_log = colorlog.getLogger(__name__)

def main():
    streamHdlr = colorlog.StreamHandler()
    streamHdlr.setFormatter(colorlog.ColoredFormatter())
    _log.addHandler(streamHdlr)
    _log.setLevel("INFO")
    
    arg_parser = argparse.ArgumentParser(
        prog="Food Finder",
        description="Search tool for food recipes from one or more ingredients "
                    "given as input by the user."
    )
    with open("./VERSION", "r") as version_file:
        version = version_file.readline()
    arg_parser.add_argument("--version",
        action="version",
        version="%(prog)s {}".format(version)
    )

    args = arg_parser.parse_args()

if __name__ == "__main__":
    main()

