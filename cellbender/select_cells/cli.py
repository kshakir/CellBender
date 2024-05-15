"""Command-line tool functionality for select-cells."""

from cellbender.base_cli import AbstractCLI, get_version
from cellbender.select_cells.run import run_select_cells

import logging
import os
import sys
import argparse


class CLI(AbstractCLI):
    """CLI implements AbstractCLI from the cellbender package."""

    def __init__(self):
        self.name = 'select-cells'
        self.args = None

    def get_name(self) -> str:
        return self.name

    @staticmethod
    def validate_args(args: argparse.Namespace) -> argparse.Namespace:
        """Validate parsed arguments."""

        # Ensure that if there's a tilde for $HOME in the file path, it works.
        try:
            args.input_file = os.path.expanduser(args.input_file)
            args.output_file = os.path.expanduser(args.output_file)
            if args.selected_barcodes is not None:
                args.selected_barcodes = os.path.expanduser(args.selected_barcodes)
        except TypeError:
            raise ValueError("Problem with provided input and output paths.")

        return args

    @staticmethod
    def run(args) -> None:
        """Run the main tool functionality on parsed arguments."""

        # Run the tool.
        return main(args)


# TODO: function is mostly copy/pasted from cbrb. Deduplicate
def setup_and_logging(args):
    """Take command-line input, parse arguments, and run tests or tool."""

    # Send logging messages to stdout as well as a log file.
    file_dir, file_base = os.path.split(args.output_file)
    file_name = os.path.splitext(os.path.basename(file_base))[0]
    log_file = os.path.join(file_dir, file_name + ".log")
    logger = logging.getLogger('cellbender')  # name of the logger
    logger.setLevel(logging.INFO if not args.debug else logging.DEBUG)
    formatter = logging.Formatter('cellbender:select-cells: %(message)s')
    file_handler = logging.FileHandler(filename=log_file, mode='w', encoding='UTF-8')
    console_handler = logging.StreamHandler()
    file_handler.setFormatter(formatter)  # set the file format
    console_handler.setFormatter(formatter)  # use the same format for stdout
    logger.addHandler(file_handler)  # log to file
    logger.addHandler(console_handler)  # log to stdout

    # Log the command as typed by user.
    logger.info("Command:\n"
                + ' '.join(['cellbender', 'select-cells'] + sys.argv[2:]))
    logger.info("CellBender " + get_version())

    return args, file_handler


def main(args) -> None:
    """Take command-line input, parse arguments, and run tests or tool."""
    args, file_handler = setup_and_logging(args)

    # Run the tool.
    run_select_cells(args)
    file_handler.close()
