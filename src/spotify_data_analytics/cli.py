import argparse
from pathlib import Path
from typing import TYPE_CHECKING

from .filtering import MaxThresholdFilter, MinThresholdFilter, RangeFilter
from .settings import (
    AnalyzeCorrelationsSettings,
    PlotCorrelationsSettings,
    PlotGamSettings,
)

if TYPE_CHECKING:
    from .filtering import FilterRule

__all__ = [
    "get_analyze_correlations_arguments",
    "get_plot_correlations_arguments",
    "get_plot_gam_arguments",
]


def get_analyze_correlations_arguments() -> AnalyzeCorrelationsSettings:
    parser = argparse.ArgumentParser(
        description="Calculate and analyze correlations between "
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
        default=Path("data/significance/popularity_correlations.csv"),
        help="Path to save the output significance analysis CSV file.",
    )
    _ = parser.add_argument(
        "--method",
        type=str,
        choices=["pearson", "spearman"],
        default="spearman",
        help="Statistical correlation method to use.",
    )
    _ = parser.add_argument(
        "--alpha",
        type=float,
        default=0.05,
        help="Significance level (alpha) for hypothesis testing.",
    )
    _ = parser.add_argument(
        "--min-threshold",
        nargs=2,
        action="append",
        metavar=("COLUMN", "VALUE"),
        help="Add a minimum threshold filter "
        + "(e.g., --min-threshold popularity 10)",
    )
    _ = parser.add_argument(
        "--max-threshold",
        nargs=2,
        action="append",
        metavar=("COLUMN", "VALUE"),
        help="Add a maximum threshold filter "
        + "(e.g., --max-threshold duration_ms 360000)",
    )
    _ = parser.add_argument(
        "--range",
        nargs=3,
        action="append",
        metavar=("COLUMN", "MIN", "MAX"),
        help="Add a range filter (e.g., --range duration_ms 120000 360000)",
    )

    namespace = parser.parse_args()

    filter_rules: list[FilterRule] = []

    min_thresholds: list[list[str]] | None = namespace.min_threshold  # pyright: ignore[reportAny]
    if min_thresholds:
        for column, value_string in min_thresholds:
            filter_rules.append(
                MinThresholdFilter(
                    column=column,
                    threshold=float(value_string),
                )
            )

    max_thresholds: list[list[str]] | None = namespace.max_threshold  # pyright: ignore[reportAny]
    if max_thresholds:
        for column, value_string in max_thresholds:
            filter_rules.append(
                MaxThresholdFilter(
                    column=column,
                    threshold=float(value_string),
                )
            )

    ranges: list[list[str]] | None = namespace.range  # pyright: ignore[reportAny]
    if ranges:
        for column, min_str, max_str in ranges:
            filter_rules.append(
                RangeFilter(
                    column=column,
                    min_value=float(min_str),
                    max_value=float(max_str),
                )
            )

    return AnalyzeCorrelationsSettings(
        input_path=namespace.input,  # pyright: ignore[reportAny]
        output_path=namespace.output,  # pyright: ignore[reportAny]
        method=namespace.method,  # pyright: ignore[reportAny]
        alpha=namespace.alpha,  # pyright: ignore[reportAny]
        filters=filter_rules,
    )


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
        default=Path("data/graphs/popularity_correlations.png"),
        help="Path to save the output PNG graph.",
    )
    _ = parser.add_argument(
        "--method",
        type=str,
        choices=["pearson", "spearman"],
        default="spearman",
        help="Statistical correlation method to use.",
    )
    _ = parser.add_argument(
        "--title",
        type=str,
        default="Spearman Correlation Between Popularity and Metrics",
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
    _ = parser.add_argument(
        "--max-threshold",
        nargs=2,
        action="append",
        metavar=("COLUMN", "VALUE"),
        help="Add a maximum threshold filter "
        + "(e.g., --max-threshold duration_ms 360000)",
    )
    _ = parser.add_argument(
        "--range",
        nargs=3,
        action="append",
        metavar=("COLUMN", "MIN", "MAX"),
        help="Add a range filter (e.g., --range duration_ms 120000 360000)",
    )

    namespace = parser.parse_args()

    filter_rules: list[FilterRule] = []

    min_thresholds: list[list[str]] | None = namespace.min_threshold  # pyright: ignore[reportAny]
    if min_thresholds:
        for column, value_string in min_thresholds:
            filter_rules.append(
                MinThresholdFilter(
                    column=column,
                    threshold=float(value_string),
                )
            )

    max_thresholds: list[list[str]] | None = namespace.max_threshold  # pyright: ignore[reportAny]
    if max_thresholds:
        for column, value_string in max_thresholds:
            filter_rules.append(
                MaxThresholdFilter(
                    column=column,
                    threshold=float(value_string),
                )
            )

    ranges: list[list[str]] | None = namespace.range  # pyright: ignore[reportAny]
    if ranges:
        for column, min_str, max_str in ranges:
            filter_rules.append(
                RangeFilter(
                    column=column,
                    min_value=float(min_str),
                    max_value=float(max_str),
                )
            )

    return PlotCorrelationsSettings(
        input_path=namespace.input,  # pyright: ignore[reportAny]
        output_path=namespace.output,  # pyright: ignore[reportAny]
        method=namespace.method,  # pyright: ignore[reportAny]
        title=namespace.title,  # pyright: ignore[reportAny]
        filters=filter_rules,
    )


def get_plot_gam_arguments() -> PlotGamSettings:
    parser = argparse.ArgumentParser(
        description="Fit and evaluate a Generalized Additive Model (GAM) "
        + "for Spotify track length and popularity.",
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
        default=Path("data/graphs/duration_popularity_gam.png"),
        help="Path to save the output GAM graph.",
    )
    _ = parser.add_argument(
        "--title",
        type=str,
        default="Non-Linear Effect of Track Length on Spotify Popularity",
        help="Title to give the graph.",
    )
    _ = parser.add_argument(
        "--n-splines",
        type=int,
        default=12,
        help="Number of splines for the smooth term.",
    )
    _ = parser.add_argument(
        "--n-grid",
        type=int,
        default=200,
        help="Number of points in the prediction grid.",
    )
    _ = parser.add_argument(
        "--scale-divisor",
        type=float,
        default=60000.0,
        help="Value to divide the feature column by during transformation.",
    )
    _ = parser.add_argument(
        "--min-threshold",
        nargs=2,
        action="append",
        metavar=("COLUMN", "VALUE"),
        help="Add a minimum threshold filter (e.g., --min-threshold popularity 10)",
    )
    _ = parser.add_argument(
        "--max-threshold",
        nargs=2,
        action="append",
        metavar=("COLUMN", "VALUE"),
        help="Add a maximum threshold filter (e.g., --max-threshold duration_ms 360000)",
    )
    _ = parser.add_argument(
        "--range",
        nargs=3,
        action="append",
        metavar=("COLUMN", "MIN", "MAX"),
        help="Add a range filter (e.g., --range duration_ms 120000 360000)",
    )

    namespace = parser.parse_args()

    filter_rules: list[FilterRule] = []

    min_thresholds: list[list[str]] | None = namespace.min_threshold  # pyright: ignore[reportAny]
    if min_thresholds:
        for column, value_string in min_thresholds:
            filter_rules.append(
                MinThresholdFilter(
                    column=column,
                    threshold=float(value_string),
                )
            )

    max_thresholds: list[list[str]] | None = namespace.max_threshold  # pyright: ignore[reportAny]
    if max_thresholds:
        for column, value_string in max_thresholds:
            filter_rules.append(
                MaxThresholdFilter(
                    column=column,
                    threshold=float(value_string),
                )
            )

    ranges: list[list[str]] | None = namespace.range  # pyright: ignore[reportAny]
    if ranges:
        for column, min_str, max_str in ranges:
            filter_rules.append(
                RangeFilter(
                    column=column,
                    min_value=float(min_str),
                    max_value=float(max_str),
                )
            )

    return PlotGamSettings(
        input_path=namespace.input,  # pyright: ignore[reportAny]
        output_path=namespace.output,  # pyright: ignore[reportAny]
        title=namespace.title,  # pyright: ignore[reportAny]
        n_splines=namespace.n_splines,  # pyright: ignore[reportAny]
        n_grid=namespace.n_grid,  # pyright: ignore[reportAny]
        scale_divisor=namespace.scale_divisor,  # pyright: ignore[reportAny]
        filters=filter_rules,
    )
