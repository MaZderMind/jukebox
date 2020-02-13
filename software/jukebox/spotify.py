import os

import spotipy

from playback_handler import PlaybackHandler


class Spotify(PlaybackHandler):
    SCOPE = 'user-modify-playback-state,user-read-playback-state,user-read-currently-playing'

    def __init__(self, conf):
        self.currently_playing_uri = None
        self.conf = conf['spotify']
        self.spotify = None
        self.device = None

    def login(self):
        print("logging into spotify connect account")
        token = self._acquire_token()
        self.spotify = spotipy.Spotify(auth=token)
        self.device = self._find_device()

    def _acquire_token(self):
        cache_dir = os.path.expanduser(self.conf['auth_token_storage_dir'])
        os.makedirs(cache_dir, exist_ok=True)

        token = spotipy.util.prompt_for_user_token(
            self.conf['username'],
            Spotify.SCOPE,
            client_id=self.conf['client_id'],
            client_secret=self.conf['client_secret'],
            redirect_uri='http://localhost/',
            cache_path=os.path.join(cache_dir, 'spotify-token-cache-' + self.conf['username']))

        return token

    def _find_device(self):
        all_devices = self.spotify.devices()['devices']
        device_name = self.conf['device_name'].lower()
        device_info = next(device for device in all_devices
                           if device['name'].lower() == device_name)

        print('found device', device_info)
        return device_info

    def play(self, uri):
        if not uri.startswith('spotify:'):
            uri = 'spotify:' + uri

        self.currently_playing_uri = uri
        self.spotify.volume(100, device_id=self.device['id'])
        self.spotify.start_playback(device_id=self.device['id'], context_uri=uri)

    def pause(self):
        self.currently_playing_uri = None
        self.spotify.pause_playback(device_id=self.device['id'])

    def volume(self, volume):
        self.spotify.volume(volume, device_id=self.device['id'])

    def is_playing(self):
        playback_info = self.spotify.current_playback()
        if playback_info is None:
            return False

        is_playing = bool(playback_info.get('is_playing'))

        context = playback_info.get('context')
        is_playing_correct_playlist = context is not None and context.get('uri') == self.currently_playing_uri

        device = playback_info.get('device', None)
        is_playing_on_device = device is not None and device.get('id') == self.device['id']

        return is_playing and is_playing_on_device and is_playing_correct_playlist
