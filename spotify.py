import requests
import urllib.parse

class Spotify(object):
	def __init__(self, api_token):
		self.api_token = api_token

	# first result is most likely the song user searched for
	def song_search(self, artist, track):
		query = urllib.parse.quote(f'{artist} {track}')
		url = f"https://api.spotify.com/v1/search?q={query}&type=track"
		response = requests.get(
			url,
			headers={
				"Content-Type": "application/json",
				"Authorization": f"Bearer {self.api_token}"
			}
		)
		response_json = response.json()

		results = response_json['tracks']['items']
		if results:

			return results[0]['id']
		else:
			raise Exception(f"No song found for {artist} = {track}")


	def sp_add_song(self, song_id):
		url = "https://api.spotify.com/v1/me/tracks"
		reponse = requests.put(
			url,
			json ={
				"ids": [song_id]
			},
			headers={
				"Content-Type": "application/json"
				"Authorization": f"Bearer {self.api_token}"
			}
		)

		return reponse.ok
