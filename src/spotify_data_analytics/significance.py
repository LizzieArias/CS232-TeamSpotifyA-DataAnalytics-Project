from typing import Literal

import polars as pl
from scipy.stats import pearsonr, spearmanr

__all__ = ["CorrelationSignificanceAnalyzer"]


class CorrelationSignificanceAnalyzer:
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

    def compute_significance(
        self,
        method: Literal["pearson", "spearman"] = "pearson",
    ) -> dict[str, tuple[float, float]]:
        df_collected = self.lazy_frame.select(  # type: ignore[reportArgumentType]
            [self.target] + self.features
        ).collect()
        target_series = df_collected.get_column(self.target)

        results: dict[str, tuple[float, float]] = {}
        for feature in self.features:
            feature_series = df_collected.get_column(feature)

            pair_df = pl.DataFrame(
                {self.target: target_series, feature: feature_series}
            )

            if feature == "tempo":
                pair_df = pair_df.filter(pl.col("tempo").is_between(60, 200))

            x = pair_df.get_column(feature).to_numpy()  # type: ignore[reportArgumentType]
            y = pair_df.get_column(self.target).to_numpy()  # type: ignore[reportArgumentType]

            if method == "pearson":
                correlation, p_value = pearsonr(x, y)
            elif method == "spearman":
                correlation, p_value = spearmanr(x, y)

            results[feature] = (float(correlation), float(p_value))

        return results
