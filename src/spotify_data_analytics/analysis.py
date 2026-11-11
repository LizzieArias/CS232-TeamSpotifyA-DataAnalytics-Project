from typing import Literal

import numpy as np
import polars as pl
from scipy.stats import kruskal, pearsonr, spearmanr

__all__ = ["CorrelationAnalyzer", "InteractionAnalyzer", "GenreAnalyzer"]


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
                lf = lf.filter(pl.col("tempo").is_between(60, 200))

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
            lf = lf.filter(pl.col("tempo").is_between(60, 200))

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


class GenreAnalyzer:
    __slots__: tuple[str, ...] = (
        "tracks_lazy_frame",
        "track_genres_lazy_frame",
        "genres_lazy_frame",
        "features",
    )
    tracks_lazy_frame: pl.LazyFrame
    track_genres_lazy_frame: pl.LazyFrame
    genres_lazy_frame: pl.LazyFrame
    features: list[str]

    def __init__(
        self,
        tracks_lazy_frame: pl.LazyFrame,
        track_genres_lazy_frame: pl.LazyFrame,
        genres_lazy_frame: pl.LazyFrame,
        features: list[str],
    ) -> None:
        self.tracks_lazy_frame = tracks_lazy_frame
        self.track_genres_lazy_frame = track_genres_lazy_frame
        self.genres_lazy_frame = genres_lazy_frame
        self.features = features

    def compute_kruskal_wallis(self, min_tracks: int = 30) -> pl.DataFrame:
        joined_lf = (
            self.tracks_lazy_frame.join(  # type: ignore[reportArgumentType]
                self.track_genres_lazy_frame,
                on="track_id",
                how="inner",
            )
            .join(self.genres_lazy_frame, on="genre_id", how="inner")
            .select(["genre_name", "track_id"] + self.features)
        )

        filtered_lf = joined_lf.filter(
            pl.len().over("genre_name") >= min_tracks
        )

        filtered_df = filtered_lf.collect()

        results: list[dict[str, str | float]] = []

        for feature in self.features:
            feature_data = filtered_df.select(["genre_name", feature])

            if feature == "tempo":
                feature_data = feature_data.filter(
                    pl.col("tempo").is_between(60, 200)
                )

            groups = [
                group.get_column(feature).to_numpy()
                for _, group in feature_data.group_by("genre_name")
                if len(group) > 0
            ]

            if len(groups) > 1:
                statistic, p_value = kruskal(*groups)
            else:
                statistic, p_value = 0.0, 1.0

            results.append(
                {
                    "feature": feature,
                    "h_statistic": float(statistic),
                    "p_value": float(p_value),
                }
            )

        return pl.DataFrame(results).sort("h_statistic", descending=True)
