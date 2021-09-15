import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import youtube_dl

class Playlist(object):
	def __init__(self, id, title):
		self.id = id
		self.title = title


class Song(object):
	def __init__(self, artist, track):
		self.artist = artist
		self.track = track


class YouTube(object):
	def __init__(self, credentials_location):
		scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

		# copied from Youtube Web API
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        credentials_location, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    self.youtube_client = youtube_client


	def get_playlist(self):
		request = self.youtube_client.playlists().list(
			part="id, snippet",
			maxResults = 50,
			mine=True
		)
		response = request.execute()

		playlists = [Playlist(item['id'], item['snippet']['title']) for playlist in response['items']]

		return playlists

	def get_ytvids(self, playlist_id):
		songs = []

		request = self.youtube_client.playlistItems().list(
			playlistId = playlist_id,
			part="id, snippet"
		)
		response = request.execute()

		## adds new yt vids based off search to final list
		for item in response['items']:
			video_id = item['snippet']['resourceId']['videoId']
			artist,track = self.get_vid_data(video_id)
			if(artist and track):
				songs.append(Song(artist, track))

		return songs

	def get_vid_data(self, video_id):
		yt_url = f"https://www.youtube.com/watch?v={video_id}"

		video = youtube_dl.YoutubeDL({'quiet': True}).extract_info(
			yt_url, download=False
		)

		artist = video['artist']
		track = video['track']

		return artist, track


