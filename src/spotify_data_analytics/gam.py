from typing import TYPE_CHECKING

from pygam import LinearGAM, s

if TYPE_CHECKING:
    import numpy as np
    import numpy.typing as npt
    import polars as pl

__all__ = ["GamAnalyzer"]


class GamAnalyzer:
    __slots__: tuple[str, ...] = ("lazy_frame", "target", "feature")
    lazy_frame: pl.LazyFrame
    target: str
    feature: str

    def __init__(
        self,
        lazy_frame: pl.LazyFrame,
        target: str,
        feature: str,
    ) -> None:
        self.lazy_frame = lazy_frame
        self.target = target
        self.feature = feature

    def fit_and_evaluate(
        self,
        n_splines: int = 12,
        n_grid: int = 200,
    ) -> tuple[
        npt.NDArray[np.float64],
        npt.NDArray[np.float64],
        npt.NDArray[np.float64],
        npt.NDArray[np.float64],
        npt.NDArray[np.float64],
        LinearGAM,
    ]:
        df_collected = self.lazy_frame.select(  # type: ignore[reportArgumentType]
            [self.target, self.feature]
        ).collect()

        x = df_collected.select(self.feature).to_numpy()
        y = df_collected.select(self.target).to_numpy().ravel()

        gam = LinearGAM(s(0, n_splines=n_splines))
        _ = gam.fit(x, y)

        xx = gam.generate_X_grid(term=0, n=n_grid)
        prediction = gam.predict(xx)
        confidence_intervals = gam.confidence_intervals(xx, width=0.95)

        return x, y, xx[:, 0], prediction, confidence_intervals, gam
