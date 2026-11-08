import matplotlib.pyplot as plt

from spotify_data_analytics import (
    CorrelationAnalyzer,
    DataFilterPipeline,
    DataLoader,
    create_correlation_bar_chart,
    get_plot_correlations_arguments,
)


def main() -> None:
    settings = get_plot_correlations_arguments()

    data_loader = DataLoader(
        settings.input_path,
        settings.target_column,
        settings.features,
    )
    raw_data = data_loader.load_and_clean()

    pipeline = DataFilterPipeline(rules=settings.filters)
    filtered_data = pipeline.apply(raw_data)

    analyzer = CorrelationAnalyzer(
        filtered_data,
        settings.target_column,
        settings.features,
    )
    correlations = analyzer.compute_correlations(method="pearson")

    fig, _ = create_correlation_bar_chart(correlations, settings.title)

    settings.output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(settings.output_path, dpi=300)  # pyright: ignore[reportUnknownMemberType]

    plt.close(fig)


if __name__ == "__main__":
    main()
