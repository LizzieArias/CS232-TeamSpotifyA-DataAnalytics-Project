from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from pathlib import Path

    from .filtering import FilterRule

__all__ = [
    "AnalyzeCorrelationsSettings",
    "PlotCorrelationsSettings",
    "PlotGamSettings",
    "PlotInteractionsSettings",
]


@dataclass(frozen=True)
class AnalyzeCorrelationsSettings:
    input_path: Path
    output_path: Path
    method: Literal["pearson", "spearman"]
    alpha: float
    target_column: str = "popularity"
    filters: list["FilterRule"] = field(default_factory=list)
    features: list[str] = field(
        default_factory=lambda: [
            "danceability",
            "energy",
            "tempo",
            "loudness",
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
    method: Literal["pearson", "spearman"]
    title: str
    target_column: str = "popularity"
    filters: list["FilterRule"] = field(default_factory=list)
    features: list[str] = field(
        default_factory=lambda: [
            "danceability",
            "energy",
            "tempo",
            "loudness",
            "speechiness",
            "acousticness",
            "instrumentalness",
            "liveness",
            "valence",
        ]
    )


@dataclass(frozen=True)
class PlotGamSettings:
    input_path: Path
    output_path: Path
    title: str
    n_splines: int = 12
    n_grid: int = 200
    target_column: str = "popularity"
    feature_column: str = "duration_ms"
    scale_divisor: float = 60000.0
    filters: list["FilterRule"] = field(default_factory=list)


@dataclass(frozen=True)
class PlotInteractionsSettings:
    input_path: Path
    graph_output_path: Path
    stats_output_path: Path
    method: Literal["pearson", "spearman"]
    title: str
    target_column: str = "popularity"
    filters: list["FilterRule"] = field(default_factory=list)
    features: list[str] = field(
        default_factory=lambda: [
            "danceability",
            "energy",
            "tempo",
            "loudness",
            "speechiness",
            "acousticness",
            "instrumentalness",
            "liveness",
            "valence",
        ]
    )
