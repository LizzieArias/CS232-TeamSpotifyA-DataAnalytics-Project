import matplotlib.pyplot as plt
import polars as pl

from spotify_data_analytics import (
    DataFilterPipeline,
    DataLoader,
    ExpressionTransformRule,
    GamAnalyzer,
    MaxThresholdFilter,
    MinThresholdFilter,
    create_gam_fit,
    get_plot_gam_arguments,
    save_figure,
)


def main() -> None:
    settings = get_plot_gam_arguments()

    data_loader = DataLoader(
        file_path=settings.input_path,
        target=settings.target_column,
        features=[settings.feature_column],
    )
    raw_data = data_loader.load_and_clean()

    pipeline = DataFilterPipeline(rules=settings.filters)

    _ = pipeline.add_rule(
        ExpressionTransformRule(
            (pl.col(settings.feature_column) / settings.scale_divisor).alias(
                "duration_min"
            )
        )
    )

    _ = pipeline.add_rule(
        MinThresholdFilter(column="duration_min", threshold=1.0)
    )
    _ = pipeline.add_rule(
        MaxThresholdFilter(column="duration_min", threshold=10.0)
    )

    filtered_data = pipeline.apply(raw_data)

    analyzer = GamAnalyzer(
        filtered_data,
        target=settings.target_column,
        feature="duration_min",
    )
    x, y, x_grid, prediction, confidence_intervals, _ = (
        analyzer.fit_and_evaluate(
            n_splines=settings.n_splines,
            n_grid=settings.n_grid,
        )
    )

    fig, _ = create_gam_fit(
        x,
        y,
        x_grid,
        prediction,
        confidence_intervals,
        title=settings.title,
    )
    save_figure(fig, settings.output_path)
    plt.close(fig)


if __name__ == "__main__":
    main()
