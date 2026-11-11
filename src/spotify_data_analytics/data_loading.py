from pathlib import Path
from typing import TYPE_CHECKING

import polars as pl

if TYPE_CHECKING:
    import os

__all__ = ["DataLoader"]


class DataLoader:
    __slots__: tuple[str, ...] = (
        "file_path",
        "target",
        "features",
    )
    file_path: Path
    target: str
    features: list[str]

    def __init__(
        self,
        file_path: str | os.PathLike[str],
        target: str,
        features: list[str],
    ) -> None:
        self.file_path = Path(file_path)
        self.target = target
        self.features = features

    def load_and_clean(self) -> pl.LazyFrame:
        if not self.file_path.exists():
            raise FileNotFoundError(f"CSV file not found at: {self.file_path}")

        cols_to_select = [self.target] + self.features

        return pl.scan_csv(self.file_path).select(cols_to_select).drop_nulls()  # type: ignore[reportArgumentType]
