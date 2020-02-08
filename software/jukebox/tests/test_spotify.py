import pytest

from spotify import Spotify


class SpotifyClientMock():
    def __init__(self):
        self._current_playback = None

    def current_playback(self):
        return self._current_playback

    def set_current_playback(self, current_playback):
        self._current_playback = current_playback


@pytest.fixture
def spotify_handler():
    spotify = Spotify(conf={'spotify': {}})
    spotify.device = {'id': '42'}
    spotify.spotify = SpotifyClientMock()
    return spotify


@pytest.mark.parametrize("current_playback", [
    None,
    {'is_playing': None},
    {'is_playing': False},
    {'is_playing': True},
    {'context': None},
    {'context': {}},
    {'context': {'uri': None}},
    {'device': None},
    {'device': {}},
    {'device': {'id': None}},
])
def test_is_playing_handles_all_kinds_of_null(spotify_handler, current_playback):
    spotify_handler.spotify.set_current_playback(current_playback)
    assert spotify_handler.is_playing() is False
