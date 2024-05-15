import argparse


def add_subparser_args(subparsers: argparse) -> argparse:
    """Add tool-specific arguments for select-cells.

    Args:
        subparsers: Parser object before addition of arguments specific to
            remove-background.

    Returns:
        parser: Parser object with additional parameters.

    """

    subparser = subparsers.add_parser("select-cells",
                                      description="Work in progress: Cell Selection.",
                                      help="Work in progress: Cell Selection.",
                                      formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    subparser.add_argument("--input", nargs=None, type=str,
                           dest='input_file',
                           required=True,
                           help="Data file on which to run tool. Data must be "
                                "un-filtered: it should include empty droplets. "
                                "The following input formats are supported: "
                                "CellRanger v2 and v3 (.h5 or the directory that "
                                "contains the .mtx file), Dropseq "
                                "DGE (.txt or .txt.gz), BD Rhapsody (.csv or "
                                ".csv.gz), AnnData (.h5ad), and Loom (.loom).")
    subparser.add_argument("--barcodes", nargs=None, type=str,
                           dest='selected_barcodes',
                           required=False,
                           help="File containing a list of barcodes to sub select from. "
                                "If provided, only the barcodes in this file will "
                                "be included in the output. If not provided, all "
                                "barcodes will be considered for the output. The file "
                                "should contain one barcode per line.")
    subparser.add_argument("--output", nargs=None, type=str,
                           dest='output_file',
                           required=True,
                           help="Output file location (the path must "
                                "exist, and the file name must have .h5 "
                                "extension).")
    subparser.add_argument("--debug",
                           dest="debug", action="store_true",
                           help="Including the flag --debug will log "
                                "extra messages useful for debugging.")



    return subparsers
