import scipy.sparse

from .analysis import CorrelationAnalyzer, InteractionAnalyzer
from .cli import (
    get_analyze_correlations_arguments,
    get_plot_correlations_arguments,
    get_plot_gam_arguments,
)
from .data_loading import DataLoader
from .filtering import (
    CategoryFilter,
    DataFilterPipeline,
    ExpressionTransformRule,
    FilterRule,
    MaxThresholdFilter,
    MinThresholdFilter,
    RangeFilter,
)
from .gam import GamAnalyzer
from .plotting import create_correlation_bar_chart, create_gam_fit, save_figure
from .settings import (
    AnalyzeCorrelationsSettings,
    PlotCorrelationsSettings,
    PlotGamSettings,
)
from .significance import CorrelationSignificanceAnalyzer
from .storage import CsvStorage, DataStorage, JsonStorage, create_storage

# Library-level compatibility patch for older pygam versions on modern scipy
for _class_name in ["csr_matrix", "csc_matrix", "coo_matrix", "spmatrix"]:
    _class = getattr(scipy.sparse, _class_name, None)
    if _class is not None and not hasattr(_class, "A"):  # pyright: ignore[reportAny]
        try:
            _class.A = property(lambda self: self.toarray())  # pyright: ignore[reportAny]
        except AttributeError, TypeError:
            pass

__all__ = [
    "CorrelationAnalyzer",
    "InteractionAnalyzer",
    "get_analyze_correlations_arguments",
    "get_plot_correlations_arguments",
    "get_plot_gam_arguments",
    "DataLoader",
    "CategoryFilter",
    "DataFilterPipeline",
    "ExpressionTransformRule",
    "FilterRule",
    "MaxThresholdFilter",
    "MinThresholdFilter",
    "RangeFilter",
    "GamAnalyzer",
    "create_correlation_bar_chart",
    "create_gam_fit",
    "save_figure",
    "AnalyzeCorrelationsSettings",
    "PlotCorrelationsSettings",
    "PlotGamSettings",
    "CorrelationSignificanceAnalyzer",
    "CsvStorage",
    "DataStorage",
    "JsonStorage",
    "create_storage",
]
