from typing import TYPE_CHECKING, Literal

from scipy.stats import pearsonr, spearmanr

if TYPE_CHECKING:
    import polars as pl

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
        target_array = df_collected.get_column(self.target).to_numpy()

        results: dict[str, tuple[float, float]] = {}
        for feature in self.features:
            feature_array = df_collected.get_column(feature).to_numpy()

            if method == "pearson":
                correlation, p_value = pearsonr(feature_array, target_array)
            elif method == "spearman":
                correlation, p_value = spearmanr(feature_array, target_array)

            results[feature] = (float(correlation), float(p_value))

        return results
