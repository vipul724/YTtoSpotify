import os

from youtube import Youtube
from spotify import Spotify


def run():
	yt_client = Youtube('./creds/client_secret.json')
	sp_client = Spotify(os.getenv('SPOTIFY_AUTH_TOKEN'))
	playlists = yt_client.get_playlist()

	# searches playlists
	for index, playlist in enumerate(playlists):
		print(f"{index}: {playlist.title}")
	choice = int(input("Enter your choice: "))
	pl_chosen = playlists[choice]
	print(f"You selected: {pl_chosen.title}")

	songs = yt_client.get_ytvids(pl_chosen.id)
	print(f"Attempting to add {len(songs)}")

	#Adds new songs to song output list
	for song in songs:
		spotify_song_id = sp_client.song_search(song.artist, song.track)
		if spotify_song_id:
			new_song = sp_client.sp_add_song(spotify_song_id)
			if new_song:
				print(f"Added {song.artist}")


if __name__ == '__main__'
	run()