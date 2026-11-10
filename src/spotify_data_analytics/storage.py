from typing import TYPE_CHECKING, Protocol, runtime_checkable

import polars as pl

if TYPE_CHECKING:
    from pathlib import Path

__all__ = ["DataStorage", "CsvStorage", "JsonStorage", "create_storage"]


@runtime_checkable
class DataStorage(Protocol):
    def save(self, data: pl.DataFrame | pl.LazyFrame) -> None: ...


class CsvStorage:
    __slots__: tuple[str, ...] = ("output_path",)
    output_path: Path

    def __init__(self, output_path: Path) -> None:
        self.output_path = output_path

    def save(self, data: pl.DataFrame | pl.LazyFrame) -> None:
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(data, pl.DataFrame):
            data.write_csv(self.output_path)  # type: ignore[reportArgumentType]
        else:
            data.sink_csv(self.output_path)  # type: ignore[reportArgumentType]


class JsonStorage:
    __slots__: tuple[str, ...] = ("output_path",)
    output_path: Path

    def __init__(self, output_path: Path) -> None:
        self.output_path = output_path

    def save(self, data: pl.DataFrame | pl.LazyFrame) -> None:
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(data, pl.LazyFrame):
            data = data.collect()  # type: ignore[reportArgumentType]
        data.write_json(self.output_path)


def create_storage(output_path: Path) -> DataStorage:
    suffix = output_path.suffix.lower()

    if suffix == ".csv":
        return CsvStorage(output_path)
    elif suffix == ".json":
        return JsonStorage(output_path)
    else:
        raise ValueError(
            f"Unsupported file extension '{suffix}'. "
            + "Supported formats: .csv, .json"
        )
