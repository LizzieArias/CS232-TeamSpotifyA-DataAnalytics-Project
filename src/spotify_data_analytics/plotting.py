# pyright: reportUnknownMemberType=false
from pathlib import Path
from typing import TYPE_CHECKING

import matplotlib.pyplot as plt

if TYPE_CHECKING:
    import os

    import numpy as np
    import numpy.typing as npt
    import polars as pl
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure
    from matplotlib.patches import Rectangle

__all__ = [
    "save_figure",
    "create_correlation_bar_chart",
    "create_gam_fit",
    "create_interaction_bar_chart",
]


def save_figure(figure: Figure, output_path: str | os.PathLike[str]) -> None:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=300, bbox_inches="tight")


def create_correlation_bar_chart(
    correlations: dict[str, float],
    title: str,
) -> tuple[Figure, Axes]:
    features = list(correlations.keys())
    values = list(correlations.values())

    sorted_pairs = sorted(zip(values, features), reverse=True)
    values, features = zip(*sorted_pairs)

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(
        list(features),
        list(values),
        color="skyblue",
        edgecolor="steelblue",
    )

    _ = ax.axvline(0, color="grey", linewidth=0.8, linestyle="--")
    _ = ax.set_xlabel("Correlation Coefficient", fontsize=12)
    _ = ax.set_title(title, fontsize=14, fontweight="bold")
    _ = ax.set_xlim(-1.0, 1.0)
    ax.grid(axis="x", linestyle=":", alpha=0.6)

    for bar in bars:  # pyright: ignore[reportUnknownVariableType]
        bar: Rectangle
        width = float(bar.get_width())  # pyright: ignore[reportUnknownArgumentType]
        label_x_pos = width + (0.03 if width >= 0 else -0.08)
        _ = ax.text(
            label_x_pos,
            bar.get_y() + bar.get_height() / 2,  # pyright: ignore[reportUnknownArgumentType]
            f"{width:.2f}",
            va="center",
            fontsize=10,
        )

    fig.tight_layout()
    return fig, ax


def create_gam_fit(
    x: npt.NDArray[np.float64],
    y: npt.NDArray[np.float64],
    x_grid: npt.NDArray[np.float64],
    prediction: npt.NDArray[np.float64],
    confidence_intervals: npt.NDArray[np.float64],
    title: str,
) -> tuple[Figure, Axes]:
    fig, ax = plt.subplots(figsize=(10, 6))
    _ = ax.scatter(x, y, alpha=0.05, color="black", label="Tracks")
    _ = ax.plot(
        x_grid,
        prediction,
        color="red",
        linewidth=3,
        label="GAM Fit (Smooth Spline)",
    )
    _ = ax.fill_between(
        x_grid,
        confidence_intervals[:, 0],
        confidence_intervals[:, 1],
        color="red",
        alpha=0.2,
        label="95% Confidence Interval",
    )

    _ = ax.set_title(title, fontsize=14, fontweight="bold")
    _ = ax.set_xlabel("Duration (Minutes)", fontsize=12)
    _ = ax.set_ylabel("Popularity (0-100)", fontsize=12)
    _ = ax.legend(loc="upper right")
    ax.grid(True, linestyle="--", alpha=0.5)
    fig.tight_layout()
    return fig, ax


def create_interaction_bar_chart(
    interaction_df: pl.DataFrame,
    title: str,
    top_n: int = 20,
) -> tuple[Figure, Axes]:
    df_top = interaction_df.head(top_n)

    interactions = df_top.get_column("interaction").to_list()
    correlations: list[float] = df_top.get_column("correlation").to_list()
    p_values: list[float] = df_top.get_column("p_value").to_list()

    interactions.reverse()
    correlations.reverse()
    p_values.reverse()

    fig, ax = plt.subplots(figsize=(10, 8))
    colors = [
        "skyblue" if correlation >= 0 else "lightcoral"
        for correlation in correlations
    ]
    bars = ax.barh(
        interactions,
        correlations,
        color=colors,
        edgecolor="steelblue",
    )

    _ = ax.axvline(0, color="grey", linewidth=0.8, linestyle="--")
    _ = ax.set_xlabel("Spearman Correlation Coefficient", fontsize=12)
    _ = ax.set_title(title, fontsize=14, fontweight="bold")
    _ = ax.set_xlim(-1.0, 1.0)
    ax.grid(axis="x", linestyle=":", alpha=0.6)

    for bar, p_value in zip(bars, p_values):  # pyright: ignore[reportUnknownVariableType]
        bar: Rectangle
        width = float(bar.get_width())  # pyright: ignore[reportUnknownArgumentType]
        label_x_pos = width + (0.03 if width >= 0 else -0.15)
        sig_text = f"{width:.2f} (p={p_value:.1e})"
        _ = ax.text(
            label_x_pos,
            bar.get_y() + bar.get_height() / 2,  # pyright: ignore[reportUnknownArgumentType]
            sig_text,
            va="center",
            fontsize=9,
        )

    fig.tight_layout()
    return fig, ax
