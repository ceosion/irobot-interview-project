#!/usr/bin/env python2

"""Main entry-point for the iRobot Interview Project ("food finder"). Run this
Python script as a commmand line utility to make use of it. Specify the `--help`
argument to see the built-in help documentation.

Author: Alex Richard Ford (arf4188@gmail.com)
"""

import colorlog
import argparse
import requests
import os

from enable_debug_action import EnableDebugAction

_prog_exec_name = os.path.basename(__file__)
_prog_friendly_name = "Food Finder"
_log = colorlog.getLogger("food_finder")

def main():
    streamHdlr = colorlog.StreamHandler()
    streamHdlr.setFormatter(colorlog.ColoredFormatter())
    _log.addHandler(streamHdlr)
    _log.setLevel("INFO")
    _log.info("Starting {} app!".format(_prog_friendly_name))

    arg_parser = argparse.ArgumentParser(
        prog=_prog_exec_name,
        description="Search tool for food recipes from one or more ingredients "
                    "given as input by the user.")

    with open("./VERSION", "r") as version_file:
        version = version_file.readline()
    arg_parser.add_argument("--version",
                            action="version",
                            version="%(prog)s {}".format(version))

    arg_parser.add_argument("--debug",
                            help="Enable debug logging for troubleshooting purposes.",
                            action=EnableDebugAction,
                            base_logger=_log)

    f2f_api_key = None
    try:
        with open("./secrets/f2f_api_key", "r") as key_file:
            f2f_api_key = key_file.readline().strip()
    except:
        pass

    arg_parser.add_argument("--f2f_api_key",
                            help="Your Food2Fork API key. Specifying this "
                                 "argument is required, unless the "
                                 "`./secrets/f2f_api_key` file is found. If "
                                 "the key file is found, but this argument is "
                                 "still specified, this argument takes "
                                 "precidence.",
                            default=f2f_api_key,
                            required=(f2f_api_key is None))

    arg_parser.add_argument("ingredients",
                            help="One or more ingredients that make up the "
                                 "recipe. Separate each ingredient with a "
                                 "space, surrounding ingredients which are "
                                 "multiple words with single or double "
                                 "quotes.",
                            nargs="+")

    args = arg_parser.parse_args()

    _log.debug("Received: {}".format(args))


if __name__ == "__main__":
    main()

