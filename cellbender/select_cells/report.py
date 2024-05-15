from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LogNorm


def plot_summary(
        selected_barcodes: np.ndarray,
        umi_counts: Optional[pd.Series],
        pct_intronic: Optional[pd.Series]):
    """Plot the summary of the selected cells."""

    fig = plt.figure(constrained_layout=True, figsize=(10, 8))

    if umi_counts is not None and pct_intronic is not None:
        # Get x and y min and max
        x_min = np.log10(umi_counts.min())
        x_max = np.log10(umi_counts.max())
        y_min = pct_intronic.min()
        y_max = pct_intronic.max()

    for i, (subset, title) in enumerate([(None, "All barcodes"), (selected_barcodes, "Selected barcodes")], start=1):
        plt.subplot(2, 1, i)

        if umi_counts is None or pct_intronic is None:
            _display_no_data_message()
        else:
            x_values = np.log10(umi_counts[subset].values) if subset is not None else np.log10(umi_counts.values)
            y_values = pct_intronic[subset].values if subset is not None else pct_intronic.values
            _plot_hexbin(x_values, y_values)
            plt.xlim(x_min, x_max)
            plt.ylim(y_min, y_max)

        plt.xlabel("log10(UMI counts)")
        plt.ylabel("% intronic reads")
        plt.title(title)

    return fig


def _plot_hexbin(x_values, y_values) -> None:
    plt.hexbin(
        x=x_values,
        y=y_values,
        gridsize=100,
        cmap='Blues',
        norm=LogNorm(),
    )


def _display_no_data_message() -> None:
    plt.text(
        x=0.5,
        y=0.5,
        s="No data available",
        horizontalalignment='center',
        verticalalignment='center',
        transform=plt.gca().transAxes,
    )
