import numpy as np
import pandas as pd


# TODO: Refactor io shared between CBRB and CBSC


def load_barcodes(file_path: str) -> np.ndarray:
    """Load cell barcodes from a file.

    Args:
        file_path: Path to the file containing the cell barcodes without a header.

    Returns:
        cell_barcodes: Series containing the cell barcodes.
    """

    return pd.read_csv(file_path, header=None, squeeze=True).values
