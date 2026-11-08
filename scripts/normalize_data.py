import os

import polars as pl


def normalize_dataset(
    input_csv_path: str,
    output_dir: str = "data_clean/normalized",
) -> None:
    os.makedirs(output_dir, exist_ok=True)

    raw_data = pl.scan_csv(
        input_csv_path,  # type: ignore[reportArgumentType]
        separator=",",  # type: ignore[reportArgumentType]
        quote_char='"',  # type: ignore[reportArgumentType]
        infer_schema_length=10000,  # type: ignore[reportArgumentType]
        schema_overrides={  # type: ignore[reportArgumentType]
            "track_id": pl.String,
            "artists": pl.String,
            "album_name": pl.String,
            "track_name": pl.String,
            "track_genre": pl.String,
        },
    )

    track_genres = (
        raw_data.select(["track_id", "track_genre"])
        .unique()
        .drop_nulls(["track_genre"])
    )

    genres = (
        track_genres.select("track_genre")
        .unique()
        .sort("track_genre")
        .with_row_index("genre_id", offset=1)
        .rename({"track_genre": "genre_name"})
    )

    track_genres_collected = (
        track_genres.join(genres, left_on="track_genre", right_on="genre_name")
        .select(["track_id", "genre_id"])
        .unique()
        .collect()
    )
    genres_collected = genres.collect()

    tracks_base = (
        raw_data.drop("track_genre")
        .unique(subset=["track_id"])
        .drop_nulls(["track_id"])
    )

    albums = (
        tracks_base.select("album_name")
        .unique()
        .sort("album_name")
        .drop_nulls(["album_name"])
        .with_row_index("album_id", offset=1)
    )

    tracks_with_album = tracks_base.join(albums, on="album_name", how="left")

    artists_exploded = tracks_base.select(
        ["track_id", "artists"]
    ).with_columns(
        pl.col("artists")
        .str.split(";")
        .list.eval(pl.element().str.strip_chars())
    )

    artists_exploded = artists_exploded.explode("artists").rename(
        {"artists": "artist_name"}
    )

    artists = (
        artists_exploded.select("artist_name")
        .unique()
        .sort("artist_name")
        .drop_nulls(["artist_name"])
        .with_row_index("artist_id", offset=1)
    )

    track_artists_collected = (
        artists_exploded.join(
            artists, left_on="artist_name", right_on="artist_name"
        )
        .select(["track_id", "artist_id"])
        .unique()
        .drop_nulls()
        .collect()
    )
    artists_collected = artists.collect()
    albums_collected = albums.collect()

    final_tracks_collected = (
        tracks_with_album.drop(["album_name", "artists"])
        .select(
            [
                "track_id",
                "album_id",
                "track_name",
                "popularity",
                "duration_ms",
                "explicit",
                "danceability",
                "energy",
                "key",
                "loudness",
                "mode",
                "speechiness",
                "acousticness",
                "instrumentalness",
                "liveness",
                "valence",
                "tempo",
                "time_signature",
            ]
        )
        .sort("track_id")
        .collect()
    )

    final_tracks_collected.write_csv(f"{output_dir}/tracks.csv")
    albums_collected.write_csv(f"{output_dir}/albums.csv")
    artists_collected.write_csv(f"{output_dir}/artists.csv")
    genres_collected.write_csv(f"{output_dir}/genres.csv")
    track_artists_collected.write_csv(f"{output_dir}/track_artists.csv")
    track_genres_collected.write_csv(f"{output_dir}/track_genres.csv")


if __name__ == "__main__":
    normalize_dataset(
        "data_raw/spotify-tracks-dataset-detailed.csv",
        output_dir="data_clean/normalized",
    )
