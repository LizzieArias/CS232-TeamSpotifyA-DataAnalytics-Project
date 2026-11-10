from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from .filtering import FilterRule

__all__ = ["AnalyzeCorrelationsSettings", "PlotCorrelationsSettings"]


@dataclass(frozen=True)
class AnalyzeCorrelationsSettings:
    input_path: Path
    output_path: Path
    alpha: float
    target_column: str = "popularity"
    filters: list["FilterRule"] = field(default_factory=list)
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


@dataclass(frozen=True)
class PlotCorrelationsSettings:
    input_path: Path
    output_path: Path
    title: str
    target_column: str = "popularity"
    filters: list["FilterRule"] = field(default_factory=list)
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
