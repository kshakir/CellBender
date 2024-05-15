"""Single run of select-cells, given input arguments."""
import argparse
import logging
import os
import sys
import traceback
from datetime import datetime

import numpy as np
import scipy.sparse as sp

from cellbender.remove_background.data.io import write_matrix_to_cellranger_h5
from cellbender.select_cells.data.dataset import get_dataset_obj, SingleCellRNACountsDataset
from cellbender.select_cells.report import plot_summary

import matplotlib
import matplotlib.backends.backend_pdf  # https://github.com/broadinstitute/CellBender/issues/287
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # This needs to be after matplotlib.use('Agg')


logger = logging.getLogger('cellbender')


def run_select_cells(args: argparse.Namespace) -> None:
    """The full script for the command line tool to cell selection RNA.

    Args:
        args: Inputs from the command line, already parsed using argparse.

    Note: Returns nothing, but writes output to a file(s) specified from
        command line.

    """

    # Log the start time.
    logger.info(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    logger.info("Running select-cells")

    # If the file doesn't end with .h5ad then exit with an error for now.
    if not args.input_file.endswith('.h5ad'):
        logger.error(f"Input file must be a .h5ad file. Got {args.input_file}. "
                     f"Only Optimus .h5ad files are supported for now.")
        sys.exit(1)

    try:
        dataset_obj = get_dataset_obj(args=args)

    except OSError:
        logger.error(f"OSError: Unable to open file {args.input_file}.")
        logger.error(traceback.format_exc())
        sys.exit(1)

    file_dir, file_base = os.path.split(args.output_file)
    file_name = os.path.splitext(os.path.basename(file_base))[0]

    write_selected_cell_matrix(
        file=args.output_file,
        selected_cell_matrix=dataset_obj.get_count_matrix(),
        dataset_obj=dataset_obj,
    )

    save_output_plots(
        file_dir=file_dir,
        file_name=file_name,
        dataset_obj=dataset_obj,
    )

    logger.info("Completed select-cells.")
    logger.info(datetime.now().strftime('%Y-%m-%d %H:%M:%S\n'))


def save_output_plots(file_dir: str,
                      file_name: str,
                      dataset_obj: SingleCellRNACountsDataset) -> bool:
    """Save the output summary PDF"""

    try:
        # File naming.
        summary_fig_name = os.path.join(file_dir, file_name + ".pdf")

        # Output summary plot.
        fig = plot_summary(
            selected_barcodes=dataset_obj.selected_barcodes,
            umi_counts=dataset_obj.data.get('barcode_num_fragments'),
            pct_intronic=dataset_obj.data.get('barcode_pct_reads_intronic'),
        )
        fig.savefig(summary_fig_name, bbox_inches='tight', format='pdf')
        logger.info(f"Saved summary plots as {summary_fig_name}")
        return True

    except Exception:
        logger.warning("Unable to save all plots.")
        logger.warning(traceback.format_exc())
        return False


def write_selected_cell_matrix(file: str,
                               selected_cell_matrix: sp.csc_matrix,
                               dataset_obj: SingleCellRNACountsDataset,
                               barcode_inds: np.ndarray = ...) -> bool:
    """Helper function for writing output h5 files"""

    return write_matrix_to_cellranger_h5(
        cellranger_version=3,  # always write v3 format output
        output_file=file,
        gene_names=dataset_obj.data['gene_names'],
        gene_ids=dataset_obj.data['gene_ids'],
        feature_types=dataset_obj.data['feature_types'],
        genomes=dataset_obj.data['genomes'],
        barcodes=dataset_obj.data['barcodes'][barcode_inds],
        count_matrix=selected_cell_matrix[barcode_inds, :],
    )
