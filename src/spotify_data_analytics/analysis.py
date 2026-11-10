from typing import Literal

import polars as pl

__all__ = ["CorrelationAnalyzer"]


class CorrelationAnalyzer:
    __slots__: tuple[str, ...] = ("lazy_frame", "target", "features")
    lazy_frame: pl.LazyFrame
    target: str
    features: list[str]

    def __init__(
        self,
        lazy_frame: pl.LazyFrame,
        target: str,
        features: list[str],
    ) -> None:
        self.lazy_frame = lazy_frame
        self.target = target
        self.features = features

    def compute_correlations(
        self,
        method: Literal["pearson", "spearman"] = "pearson",
    ) -> dict[str, float]:
        correlations: dict[str, float] = {}

        for feature in self.features:
            lf = self.lazy_frame
            if feature == "tempo":
                lf = lf.filter(pl.col("tempo") > 0)

            expression = pl.corr(self.target, feature, method=method).alias(
                feature
            )
            results_collected = lf.select(expression).collect()  # type: ignore[reportArgumentType]

            correlation_value = results_collected.get_column(feature).item()  # pyright: ignore[reportAny]
            correlations[feature] = (
                correlation_value if correlation_value is not None else 0.0
            )

        return correlations
