import polars as pl

from spotify_data_analytics import (
    CorrelationSignificanceAnalyzer,
    DataFilterPipeline,
    DataLoader,
    create_storage,
    get_analyze_correlations_arguments,
)


def main() -> None:
    settings = get_analyze_correlations_arguments()
    alpha = settings.alpha

    data_loader = DataLoader(
        settings.input_path,
        settings.target_column,
        settings.features,
    )
    raw_data = data_loader.load_and_clean()
    pipeline = DataFilterPipeline(rules=settings.filters)
    filtered_data = pipeline.apply(raw_data)

    analyzer = CorrelationSignificanceAnalyzer(
        filtered_data,
        settings.target_column,
        settings.features,
    )
    results = analyzer.compute_significance(method="pearson")

    df_results = pl.DataFrame(
        [
            {
                "feature": feature,
                "correlation": correlation,
                "p_value": p_value,
                "alpha": alpha,
                "is_significant": p_value < alpha,
            }
            for feature, (correlation, p_value) in results.items()
        ]
    )

    storage = create_storage(settings.output_path)
    storage.save(df_results)


if __name__ == "__main__":
    main()
