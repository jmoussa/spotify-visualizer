import spotipy
import pandas as pd
import matplotlib.pyplot as plt
from config import CLIENT_ID, CLIENT_SECRET
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
user_id = "1218881629"


def search_spotify(query: str = None):
    q = query.replace(" ", "+")
    results = sp.search(q, limit=100)
    r = results["tracks"]["items"]
    return r


def get_new_released_albums(country="US"):
    album_list = sp.new_releases(country=country)
    # for album in album_list["albums"]["items"]:
    # print(album["name"], [artist["name"] for artist in album["artists"]])
    return album_list["albums"]["items"]


def get_audio_features_for_album(album_id):
    df = pd.DataFrame(
        columns=[
            "id",
            "danceability",
            "energy",
            "key",
            "loudness",
            "speechiness",
            "acousticness",
            "instrumentalness",
            "liveness",
            "valence",
            "tempo",
            "duration_ms",
        ]
    )

    album_tracks = sp.album_tracks(album_id)
    track_id_to_name = {track["id"]: track["name"] for track in album_tracks["items"]}
    track_ids = [track["id"] for track in album_tracks["items"]]
    feature_objects_array = sp.audio_features(tracks=track_ids)

    for i in range(0, len(feature_objects_array)):
        feature = feature_objects_array[i]
        if feature:
            for key in df.keys():
                df.loc[i, key] = feature[key]

    df["name"] = df["id"].apply(lambda x: track_id_to_name[x])
    df["duration_min"] = df["duration_ms"] / 1000 / 60
    df = df.drop(columns=["duration_ms"])
    return df


def get_avg_album_scores(album_tuples):
    df = pd.DataFrame(
        columns=[
            "album_name",
            "danceability",
            "energy",
            "loudness",
            "speechiness",
            "acousticness",
            "instrumentalness",
            "liveness",
            "valence",
            "tempo",
            "duration_min",
        ]
    )

    for i in range(0, len(album_tuples)):
        feature_df = album_tuples[i][0]
        album_name = album_tuples[i][1]
        for column in df:
            if column not in ("album_name"):
                df.loc[i, column] = feature_df[column].mean()
        df.loc[i, "album_name"] = album_name
    return df


if __name__ == "__main__":
    album_list = get_new_released_albums()
    album_features_names_tuples = [(get_audio_features_for_album(album["id"]), album["name"]) for album in album_list]
    avg_df = get_avg_album_scores(album_features_names_tuples)
    print(avg_df)

    # plotting
    fig, ax = plt.subplots(3, 3, figsize=(13, 9))

    columns = avg_df.columns
    column_counter = 1
    for i in range(0, 3):
        for j in range(0, 3):
            column = columns[column_counter]
            if column != "album_name":
                ax[i, j].bar(avg_df["album_name"], avg_df[columns[column_counter]])
                ax[i, j].set_title(columns[column_counter])
            column_counter += 1
            for tick in ax[i, j].get_xticklabels():
                tick.set_rotation(90)

    plt.xticks(rotation=90)
    plt.show()
