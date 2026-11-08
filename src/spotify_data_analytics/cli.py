import argparse
from pathlib import Path

from .settings import PlotCorrelationsSettings

__all__ = ["get_plot_correlations_arguments"]


def get_plot_correlations_arguments() -> PlotCorrelationsSettings:
    parser = argparse.ArgumentParser(
        description="Generate and save a correlation bar chart between "
        + "Spotify track popularity and audio features."
    )
    _ = parser.add_argument(
        "--input",
        type=Path,
        default=Path("spotify_tracks.csv"),
        help="Path to the input Spotify CSV file.",
    )
    _ = parser.add_argument(
        "--output",
        type=Path,
        default=Path("output_graphs/popularity_correlation.png"),
        help="Path to save the output PNG graph.",
    )

    namespace = parser.parse_args()
    return PlotCorrelationsSettings(
        input_path=namespace.input,  # pyright: ignore[reportAny]
        output_path=namespace.output,  # pyright: ignore[reportAny]
    )
