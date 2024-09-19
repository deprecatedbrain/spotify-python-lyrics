import requests
import json

class SpotifyException(Exception):
    pass

class SpotifyLyrics:
    def __init__(self, sp_dc):
        self.sp_dc = sp_dc
        self.token_url = 'https://open.spotify.com/get_access_token?reason=transport&productType=web_player'
        self.lyrics_url = 'https://spclient.wg.spotify.com/color-lyrics/v2/track/'

    def get_token(self):
        if not self.sp_dc:
            raise SpotifyException('You did not provide an SP_DC token!')

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36',
            'App-platform': 'WebPlayer',
            'content-type': 'text/html; charset=utf-8',
            'cookie': f'sp_dc={self.sp_dc}',
        }

        response = requests.get(self.token_url, headers=headers)
        token_json = response.json()

        if not token_json or token_json['isAnonymous']:
            raise SpotifyException('The provided SP_DC token is incorrect!')

        return token_json['accessToken']

    def get_lyrics(self, track_id):
        token = self.get_token()
        formatted_url = f'{self.lyrics_url}{track_id}?format=json&market=from_token'
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36',
            'App-platform': 'WebPlayer',
            'authorization': f'Bearer {token}',
        }

        response = requests.get(formatted_url, headers=headers)
        return response.text
