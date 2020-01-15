#!/usr/bin/env python3
import os.path

import spotipy
import spotipy.util as util
import toml

conf = toml.load("configuration.toml")
scope = 'user-modify-playback-state,user-read-playback-state,user-read-currently-playing'
cache_dir = '~/.config/jukebox/'

cache_dir = os.path.expanduser(cache_dir)
os.makedirs(cache_dir, exist_ok=True)

token = util.prompt_for_user_token(
    conf['spotify']['username'],
    scope,
    client_id=conf['spotify']['client_id'],
    client_secret=conf['spotify']['client_secret'],
    redirect_uri='http://localhost/',
    cache_path=os.path.join(cache_dir, 'spotify-token-cache-' + conf['spotify']['username']))

spotify = spotipy.Spotify(auth=token)

all_devices = spotify.devices()['devices']
device_info = next(device for device in all_devices
                   if device['name'].lower() == conf['spotify']['device_name'].lower())

# print('found device', device_info)

playlist_uri = 'spotify:playlist:37i9dQZF1DX6GJXiuZRisr'  # Night Rider
# playlist_uri = 'spotify:playlist:37i9dQZF1DWYfQ0uxBYM90' # 60s

# spotify.start_playback(device_id=device_info['id'], context_uri=playlist_uri)
# spotify.pause_playback(device_id=device_info['id'])
# spotify.volume(50, device_id=device_info['id'])

playback = spotify.current_playback()
is_playing = playback['is_playing']
is_playing_correct_playlist = playback['context']['uri'] == playlist_uri
is_playing_on_device = playback['device']['id'] == device_info['id']
print('is_playing', is_playing, 'is_playing_correct_playlist', is_playing_correct_playlist, 'is_playing_on_device',
      is_playing_on_device)
