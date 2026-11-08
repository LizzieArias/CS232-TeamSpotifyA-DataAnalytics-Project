import argparse
from pathlib import Path
from typing import TYPE_CHECKING

from .filtering import MinThresholdFilter
from .settings import PlotCorrelationsSettings

if TYPE_CHECKING:
    from .filtering import FilterRule

__all__ = ["get_plot_correlations_arguments"]


def get_plot_correlations_arguments() -> PlotCorrelationsSettings:
    parser = argparse.ArgumentParser(
        description="Generate and save a correlation bar chart between "
        + "Spotify track popularity and audio features.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    _ = parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/normalized/tracks.csv"),
        help="Path to the input Spotify CSV file.",
    )
    _ = parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/graphs/popularity_correlation.png"),
        help="Path to save the output PNG graph.",
    )
    _ = parser.add_argument(
        "--title",
        type=str,
        default="Correlation with Track Popularity",
        help="Title to give the graph.",
    )
    _ = parser.add_argument(
        "--min-threshold",
        nargs=2,
        action="append",
        metavar=("COLUMN", "VALUE"),
        help="Add a minimum threshold filter "
        + "(e.g., --min-threshold popularity 10)",
    )

    namespace = parser.parse_args()

    filter_rules: list[FilterRule] = []

    min_threshold: list[list[str]] | None = namespace.min_threshold  # pyright: ignore[reportAny]
    if min_threshold:
        for column, value_string in min_threshold:
            filter_rules.append(
                MinThresholdFilter(
                    column=column,
                    threshold=float(value_string),
                )
            )

    return PlotCorrelationsSettings(
        input_path=namespace.input,  # pyright: ignore[reportAny]
        output_path=namespace.output,  # pyright: ignore[reportAny]
        title=namespace.title,  # pyright: ignore[reportAny]
        filters=filter_rules,
    )
