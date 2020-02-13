import feedparser

from ffplay import FFplay
from playback_handler import PlaybackHandler


class Podcast(PlaybackHandler, FFplay):
    def pause(self):
        self.stop_ffplay()

    def is_playing(self):
        return self.is_ffplay_running()

    def play(self, target):
        print("parsing feed", target)
        feed = feedparser.parse(target)
        print("parsed feed", feed["channel"]["title"], "with", len(feed["items"]), "items")
        item = feed["items"][0]
        url = next(item['href'] for item in feed["items"][0]["links"] if item['rel'] == 'enclosure')
        print("playing item", item["title"], "from", url)

        return self.start_ffplay(url)
