from typing import Protocol, runtime_checkable

import polars as pl

__all__ = [
    "FilterRule",
    "MinThresholdFilter",
    "MaxThresholdFilter",
    "RangeFilter",
    "CategoryFilter",
    "ExpressionTransformRule",
    "DataFilterPipeline",
]


@runtime_checkable
class FilterRule(Protocol):
    def apply(self, lf: pl.LazyFrame) -> pl.LazyFrame: ...


class MinThresholdFilter:
    __slots__: tuple[str, ...] = ("column", "threshold")
    column: str
    threshold: float

    def __init__(self, column: str, threshold: float) -> None:
        self.column = column
        self.threshold = threshold

    def apply(self, lf: pl.LazyFrame) -> pl.LazyFrame:
        return lf.filter(pl.col(self.column) >= self.threshold)


class MaxThresholdFilter:
    __slots__: tuple[str, ...] = ("column", "threshold")
    column: str
    threshold: float

    def __init__(self, column: str, threshold: float) -> None:
        self.column = column
        self.threshold = threshold

    def apply(self, lf: pl.LazyFrame) -> pl.LazyFrame:
        return lf.filter(pl.col(self.column) <= self.threshold)


class RangeFilter:
    __slots__: tuple[str, ...] = ("column", "min_value", "max_value")
    column: str
    min_value: float
    max_value: float

    def __init__(
        self,
        column: str,
        min_value: float,
        max_value: float,
    ) -> None:
        self.column = column
        self.min_value = min_value
        self.max_value = max_value

    def apply(self, lf: pl.LazyFrame) -> pl.LazyFrame:
        return lf.filter(
            pl.col(self.column).is_between(self.min_value, self.max_value),
        )


class CategoryFilter:
    __slots__: tuple[str, ...] = ("column", "allowed_values")
    column: str
    allowed_values: list[str]

    def __init__(self, column: str, allowed_values: list[str]) -> None:
        self.column = column
        self.allowed_values = allowed_values

    def apply(self, lf: pl.LazyFrame) -> pl.LazyFrame:
        return lf.filter(pl.col(self.column).is_in(self.allowed_values))


class ExpressionTransformRule:
    __slots__: tuple[str, ...] = ("expressions",)
    expressions: list[pl.Expr]

    def __init__(self, expressions: pl.Expr | list[pl.Expr]) -> None:
        self.expressions = (
            [expressions] if isinstance(expressions, pl.Expr) else expressions
        )

    def apply(self, lf: pl.LazyFrame) -> pl.LazyFrame:
        return lf.with_columns(self.expressions)


class DataFilterPipeline:
    __slots__: tuple[str, ...] = ("rules",)
    rules: list[FilterRule]

    def __init__(self, rules: list[FilterRule] | None = None) -> None:
        self.rules = rules or []

    def add_rule(self, rule: FilterRule) -> "DataFilterPipeline":
        self.rules.append(rule)
        return self

    def apply(self, lf: pl.LazyFrame) -> pl.LazyFrame:
        for rule in self.rules:
            lf = rule.apply(lf)
        return lf
