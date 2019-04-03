import argparse
import colorlog

_log = colorlog.getLogger("food_finder.{}".format(__name__))

class EnableDebugAction(argparse.Action):
    """An argparse Action which handles the '--debug' argument, if specified
    by the user. This sets the logging level to 'DEBUG' for the given
    base_logger provided in the constructor."""

    def __init__(self,
                 option_strings,
                 dest,
                 nargs=0,
                 const=True,
                 default=None,
                 type=None,
                 choices=None,
                 required=False,
                 help="Enables debug logging for troubleshooting purposes.",
                 metavar=None,
                 base_logger=None):
        argparse.Action.__init__(self,
                                 option_strings=option_strings,
                                 dest=dest,
                                 nargs=nargs,
                                 const=const,
                                 default=default,
                                 type=type,
                                 choices=choices,
                                 required=required,
                                 help=help,
                                 metavar=metavar)
        self.base_logger = base_logger

    def __call__(self, parser, namespace, values, option_string=None):
        self.base_logger.setLevel("DEBUG")
        _log.debug("Debug logging has been enabled!")

