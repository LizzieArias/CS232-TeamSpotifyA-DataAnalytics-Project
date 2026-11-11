import polars as pl

from spotify_data_analytics import (
    GenreAnalyzer,
    create_storage,
    get_analyze_genres_arguments,
)


def main() -> None:
    settings = get_analyze_genres_arguments()

    tracks_lf = pl.scan_csv(settings.tracks_input_path)  # type: ignore[reportArgumentType]
    track_genres_lf = pl.scan_csv(settings.track_genres_input_path)  # type: ignore[reportArgumentType]
    genres_lf = pl.scan_csv(settings.genres_input_path)  # type: ignore[reportArgumentType]

    analyzer = GenreAnalyzer(
        tracks_lazy_frame=tracks_lf,
        track_genres_lazy_frame=track_genres_lf,
        genres_lazy_frame=genres_lf,
        features=settings.features,
    )

    results_df = analyzer.compute_kruskal_wallis(
        min_tracks=settings.min_tracks,
    )

    storage = create_storage(settings.output_path)
    storage.save(results_df)


if __name__ == "__main__":
    main()
