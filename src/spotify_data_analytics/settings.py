from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from .filtering import FilterRule

__all__ = ["PlotCorrelationsSettings"]


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
