# pyright: reportUnknownMemberType=false
from typing import TYPE_CHECKING

import matplotlib.pyplot as plt

if TYPE_CHECKING:
    from pathlib import Path

    from matplotlib.axes import Axes
    from matplotlib.figure import Figure
    from matplotlib.patches import Rectangle

__all__ = ["save_figure", "create_correlation_bar_chart"]


def save_figure(figure: Figure, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
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
