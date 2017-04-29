import os
import sys
import spotipy
import spotipy.util as util
from spotipy import oauth2

SCOPE = 'playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private streaming user-follow-modify user-follow-read user-library-read user-library-modify user-read-private user-read-birthdate user-read-email user-top-read'

CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

def get_sp_oauth(username):
    return oauth2.SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, scope=SCOPE, cache_path=".cache-" + username )

def get_sp_token(username):
    sp_oauth = get_sp_oauth(username)
    token_info = sp_oauth.get_cached_token()
    if token_info:
        return token_info['access_token']
    else:
        return None

def get_auth_url(username):
    sp_oauth = get_sp_oauth(username)
    return sp_oauth.get_authorize_url()

def get_token_from_code(username, code):
    sp_oauth = get_sp_oauth(username)
    token_info = sp_oauth.get_access_token(code)
    if token_info:
        return token_info['access_token']
    else:
        return None

def get_top_tracks(token, time_range='long_term'):
    sp = spotipy.Spotify(auth=token)
    return sp.current_user_top_tracks(time_range=time_range)

def get_track_info(track_id):
    sp = spotipy.Spotify()
    return sp.track(track_id)