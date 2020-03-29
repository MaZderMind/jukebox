import os
import subprocess

import spotipy

from playback_handler import PlaybackHandler


class Spotify(PlaybackHandler):
    SCOPE = 'user-modify-playback-state,user-read-playback-state,user-read-currently-playing'

    def __init__(self, conf):
        self.currently_playing_uri = None
        self.conf = conf['spotify']
        self.spotify = None

    def login(self):
        print("logging into spotify connect account")
        self.spotify = spotipy.Spotify(oauth_manager=self._create_auth_manager())

    def _create_auth_manager(self):
        cache_dir = os.path.expanduser(self.conf['auth_token_storage_dir'])
        os.makedirs(cache_dir, exist_ok=True)

        return spotipy.oauth2.SpotifyOAuth(
            username=self.conf['username'],
            scope=Spotify.SCOPE,
            client_id=self.conf['client_id'],
            client_secret=self.conf['client_secret'],
            redirect_uri='http://localhost/',
            cache_path=os.path.join(cache_dir, 'spotify-token-cache-' + self.conf['username']))

    def _find_device(self):
        all_devices = self.spotify.devices()['devices']
        device_name = self.conf['device_name'].lower()
        try:
            device_info = next(device for device in all_devices
                               if device['name'].lower() == device_name)
        except StopIteration:
            print('did not find device', device_name, 'available devices:', [device['name'] for device in all_devices])
            print('trying to restart raspotify.service before next restart')
            subprocess.check_call(['sudo', 'systemctl', 'restart', 'raspotify.service'])
            raise

        print('found device', device_info)
        return device_info

    def play(self, uri):
        if not uri.startswith('spotify:'):
            uri = 'spotify:' + uri

        device = self._find_device()
        self.currently_playing_uri = uri
        self.spotify.volume(100, device_id=device['id'])
        self.spotify.start_playback(device_id=device['id'], context_uri=uri)

    def pause(self):
        self.currently_playing_uri = None
        device = self._find_device()
        self.spotify.pause_playback(device_id=device['id'])

    def volume(self, volume):
        device = self._find_device()
        self.spotify.volume(volume, device_id=device['id'])

    def is_playing(self):
        playback_info = self.spotify.current_playback()
        if playback_info is None:
            return False

        device = self._find_device()
        is_playing = bool(playback_info.get('is_playing'))

        context = playback_info.get('context')
        is_playing_correct_playlist = context is not None and context.get('uri') == self.currently_playing_uri

        playing_device = playback_info.get('device', None)
        is_playing_on_device = playing_device is not None and playing_device.get('id') == device['id']

        return is_playing and is_playing_on_device and is_playing_correct_playlist
