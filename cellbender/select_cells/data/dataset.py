"""Class and functions for working with a count matrix dataset."""

import argparse
import logging
from typing import Optional

import scipy.sparse as sp

from cellbender.remove_background.data.io import load_data
from cellbender.select_cells.data.io import load_barcodes


logger = logging.getLogger('cellbender')


class SingleCellRNACountsDataset:
    """Object for storing scRNA-seq count matrix data and basic manipulations
    and pre-processing (e.g. estimation of prior hyperparameters).

    Args:
        input_file: Input data file path.

    Attributes:
        input_file: Name of data source file.
        data: Loaded data as a dict, with ['matrix', 'barcodes', 'gene_names'].

    Note: Count data is kept as the original, untransformed data.  Priors are
    in terms of the transformed count data.

    """
    def __init__(self,
                 input_file: str,
                 selected_barcodes: Optional[str]):
        assert input_file is not None, "Attempting to load data, but no " \
                                       "input file was specified."
        self.input_file = input_file

        # Load the dataset.
        self.data = load_data(self.input_file)

        if self.data.get('barcode_pct_reads_intronic') is None:
            logger.warning("WARNING: No intronic read counts or percentage detected in the input data.")
        if self.data.get('barcode_num_fragments') is None:
            logger.warning("WARNING: No UMI counts detected in the input data.")

        # Filter the dataset if selected_barcodes is provided.
        if selected_barcodes is not None:
            self.selected_barcodes = load_barcodes(selected_barcodes)
        else:
            logger.warning("No barcodes selected. Using all barcodes.")
            self.selected_barcodes = self.data['barcodes']

    def get_count_matrix(self) -> sp.csc_matrix:
        """Get the count matrix."""

        return self.data['matrix'].tocsc()


def get_dataset_obj(args: argparse.Namespace) -> SingleCellRNACountsDataset:
    """Helper function that uses the argparse namespace"""

    return SingleCellRNACountsDataset(
        input_file=args.input_file,
        selected_barcodes=args.selected_barcodes,
    )
