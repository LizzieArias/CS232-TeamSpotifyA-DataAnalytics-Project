import matplotlib.pyplot as plt

from spotify_data_analytics import (
    DataFilterPipeline,
    DataLoader,
    InteractionAnalyzer,
    create_interaction_bar_chart,
    create_storage,
    get_plot_interactions_arguments,
    save_figure,
)


def main() -> None:
    settings = get_plot_interactions_arguments()

    data_loader = DataLoader(
        settings.input_path,
        settings.target_column,
        settings.features,
    )
    raw_data = data_loader.load_and_clean()

    pipeline = DataFilterPipeline(rules=settings.filters)
    filtered_data = pipeline.apply(raw_data)

    analyzer = InteractionAnalyzer(
        filtered_data,
        settings.target_column,
        settings.features,
    )
    interactions_df = analyzer.compute_interactions(method=settings.method)

    storage = create_storage(settings.stats_output_path)
    storage.save(interactions_df)

    fig, _ = create_interaction_bar_chart(
        interactions_df,
        title=settings.title,
    )
    save_figure(fig, settings.graph_output_path)
    plt.close(fig)


if __name__ == "__main__":
    main()
