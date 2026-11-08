from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

__all__ = ["PlotCorrelationsSettings"]


@dataclass(frozen=True)
class PlotCorrelationsSettings:
    input_path: Path
    output_path: Path
    target_column: str = "popularity"
    features: list[str] = field(
        default_factory=lambda: [
            "danceability",
            "energy",
            "speechiness",
            "acousticness",
            "instrumentalness",
            "liveness",
            "valence",
        ]
    )
    title: str = "Correlation with Track Popularity"
