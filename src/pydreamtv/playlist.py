from pathlib import Path
from pydreamtv.channel import Channel


class Playlist:
    def __init__(self, playlist: Path):
        """
        Load a playlist from file
        """
        if not playlist or not playlist.exists:
            raise Exception("Playlist file does not exist")

        with open(playlist, "r") as playlist_handle:
            lines = playlist_handle.readlines()

        self.channels = []
        channel = None

        for line in lines:
            if line.startswith("#EXTINF"):
                if channel:
                    self.channels.append(channel)
                channel = Channel.from_playlist_line(line)
            elif line.startswith("http"):
                if channel:
                    channel.url = line

        if channel:
            self.channels.append(channel)
