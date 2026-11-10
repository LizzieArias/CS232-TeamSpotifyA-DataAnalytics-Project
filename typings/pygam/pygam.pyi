from typing import Any, Self

import numpy as np
import numpy.typing as npt
from pygam.core import Core
from pygam.terms import MetaTermMixin

EPS = ...

class GAM(Core, MetaTermMixin):
    def __init__(
        self,
        terms=...,
        max_iter=...,
        tol=...,
        distribution=...,
        link=...,
        callbacks=...,
        fit_intercept=...,
        verbose=...,
        **kwargs,
    ) -> None: ...
    def loglikelihood(self, X, y, weights=...): ...
    def predict_mu(self, X) -> Any: ...
    def predict(self, X) -> Any: ...
    def fit(self, X, y, weights=...) -> Self: ...
    def score(self, X, y, weights=...): ...
    def deviance_residuals(self, X, y, weights=..., scaled=...): ...
    def confidence_intervals(
        self, X, width=..., quantiles=...
    ) -> Any | NDArray[Any]: ...
    def generate_X_grid(
        self, term, n=..., meshgrid=...
    ) -> (
        tuple[NDArray[Any], ...]
        | _Array[tuple[Any, Any], float64]
        | tuple[Any]
        | _Array[tuple[int, Any], float64]
    ): ...
    def partial_dependence(
        self, term, X=..., width=..., quantiles=..., meshgrid=...
    ) -> list[Any]: ...
    def summary(self) -> None: ...
    def gridsearch(
        self,
        X,
        y,
        weights=...,
        return_scores=...,
        keep_best=...,
        objective=...,
        progress=...,
        **param_grids,
    ): ...
    def sample(
        self,
        X,
        y,
        quantity=...,
        sample_at_X=...,
        weights=...,
        n_draws=...,
        n_bootstraps=...,
        objective=...,
    ) -> _Array[tuple[Any, int], float64] | Any: ...

class LinearGAM(GAM):
    def __init__(
        self,
        terms: Any = ...,
        link: Any | None = ...,
        distribution: Any | None = ...,
        constraints: Any | None = ...,
        **kwargs: Any,
    ) -> None: ...
    def fit(
        self,
        X: npt.ArrayLike,
        y: npt.ArrayLike,
        weights: npt.ArrayLike | None = ...,
        **kwargs: Any,
    ) -> Self: ...
    def predict(self, X: npt.ArrayLike) -> npt.NDArray[np.float64]: ...
    def confidence_intervals(
        self,
        X: npt.ArrayLike,
        width: float = 0.95,
        n_samples: int = 0,
    ) -> npt.NDArray[np.float64]: ...
    def generate_X_grid(
        self,
        term: int = 0,
        n: int = 100,
    ) -> npt.NDArray[np.float64]: ...
    def summary(self) -> None: ...

class LogisticGAM(GAM):
    def __init__(
        self,
        terms=...,
        max_iter=...,
        tol=...,
        callbacks=...,
        fit_intercept=...,
        verbose=...,
        **kwargs,
    ) -> None: ...
    def accuracy(self, X=..., y=..., mu=...) -> Any: ...
    def score(self, X, y) -> Any: ...
    def predict(self, X) -> Any: ...
    def predict_proba(self, X) -> Any: ...

class PoissonGAM(GAM):
    def __init__(
        self,
        terms=...,
        max_iter=...,
        tol=...,
        callbacks=...,
        fit_intercept=...,
        verbose=...,
        **kwargs,
    ) -> None: ...
    def loglikelihood(self, X, y, exposure=..., weights=...): ...
    def fit(self, X, y, exposure=..., weights=...) -> Self: ...
    def predict(self, X, exposure=...) -> Any: ...
    def gridsearch(
        self,
        X,
        y,
        exposure=...,
        weights=...,
        return_scores=...,
        keep_best=...,
        objective=...,
        **param_grids,
    ): ...

class GammaGAM(GAM):
    def __init__(
        self,
        terms=...,
        max_iter=...,
        tol=...,
        scale=...,
        callbacks=...,
        fit_intercept=...,
        verbose=...,
        **kwargs,
    ) -> None: ...

class InvGaussGAM(GAM):
    def __init__(
        self,
        terms=...,
        max_iter=...,
        tol=...,
        scale=...,
        callbacks=...,
        fit_intercept=...,
        verbose=...,
        **kwargs,
    ) -> None: ...

class ExpectileGAM(GAM):
    def __init__(
        self,
        terms=...,
        max_iter=...,
        tol=...,
        scale=...,
        callbacks=...,
        fit_intercept=...,
        expectile=...,
        verbose=...,
        **kwargs,
    ) -> None: ...
    def fit_quantile(
        self, X, y, quantile, max_iter=..., tol=..., weights=...
    ) -> Self: ...
