from typing import Literal

import numpy as np
import polars as pl
from scipy.stats import pearsonr, spearmanr

__all__ = ["CorrelationAnalyzer", "InteractionAnalyzer"]


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


class InteractionAnalyzer:
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

    def compute_interactions(
        self,
        method: Literal["spearman", "pearson"] = "spearman",
    ) -> pl.DataFrame:
        expressions: list[pl.Expr] = []
        interaction_names: list[str] = []

        feature_count = len(self.features)
        for i in range(feature_count):
            for j in range(i + 1, feature_count):
                feature_1 = self.features[i]
                feature_2 = self.features[j]

                product_name = f"{feature_1}_x_{feature_2}"
                expressions.append(
                    (pl.col(feature_1) * pl.col(feature_2)).alias(product_name)
                )
                interaction_names.append(product_name)

                ratio_name = f"{feature_1}_div_{feature_2}"
                expressions.append(
                    (pl.col(feature_1) / (pl.col(feature_2) + 1e-6)).alias(
                        ratio_name
                    )
                )
                interaction_names.append(ratio_name)

        lf = self.lazy_frame
        if "tempo" in self.features:
            lf = lf.filter(pl.col("tempo") > 0)

        df = (
            lf.with_columns(expressions)  # type: ignore[reportArgumentType]
            .select([self.target] + interaction_names)
            .collect()
        )

        y = df.get_column(self.target).to_numpy()

        results: list[dict[str, str | float]] = []
        for name in interaction_names:
            x = df.get_column(name).to_numpy()
            mask = np.isfinite(x) & np.isfinite(y)
            x_clean = x[mask]
            y_clean = y[mask]

            if len(x_clean) < 2:
                correlation, p_value = 0.0, 1.0
            else:
                if method == "spearman":
                    result = spearmanr(x_clean, y_clean)
                    correlation = float(result.statistic)
                    p_value = float(result.pvalue)
                else:
                    result = pearsonr(x_clean, y_clean)
                    correlation = float(result.statistic)
                    p_value = float(result.pvalue)

            results.append(
                {
                    "interaction": name,
                    "correlation": correlation,
                    "p_value": p_value,
                }
            )

        return pl.DataFrame(results).sort(
            pl.col("correlation").abs(),
            descending=True,
        )
