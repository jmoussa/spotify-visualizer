import altair as alt

from utils import get_new_released_albums, get_audio_features_for_album, get_avg_album_scores

if __name__ == "__main__":
    album_list = get_new_released_albums()
    album_features_names_tuples = [(get_audio_features_for_album(album["id"]), album["name"]) for album in album_list]
    avg_df = get_avg_album_scores(album_features_names_tuples)
    print(avg_df)

    columns = avg_df.columns
    column_counter = 1
    for i in range(0, 3):
        for j in range(0, 3):
            column = columns[column_counter]
            if column != "album_name":
                final_chart = (
                    alt.Chart(avg_df)
                    .mark_bar()
                    .encode(y="album_name", x=columns[column_counter], tooltip=f"{columns[column_counter]}",)
                    .properties(height=700, width=1080)
                    .interactive()
                )

                final_chart.save(f"./html/{columns[column_counter]}.html")
            column_counter += 1
