# pydreamtv

## Stream IPTV to Discord.

Beware, this is in early stages but it does work. It needs a bit to get it going, but if you understand IPTV providers and how Discord voice chat works then it should make sense. The instructions are brief and makes assumptions that you understand the individual parts rather than going into details on how each stage works.

This janky bot does the following:

* Listens to commands on a server for `tv` commands
* Controls an instance of `mpv` via these commands
* The instance of `mpv` is used by Discord to stream the video
* A desktop audio loopback is needed to get the `mpv` sound to Discord. `virtualmic` is used for that.
* Downloads M3U and XMLTV files from your IPTV provider
* Stored the data in a MySQL database
* Searches and switches channels by looking stuff up in the database and controlling `mpv`

### What you'll need

* This has only been tested in Linux, so for now you need Linux
* Python 3+
* MPV installed and working
* MySQL installed somewhere and working
* Discord installed and working
* A Discord account and server
* A registered application in Discord with a bot token
* An IPTV account along with:
    * A URL for the channel listings, preferrably as an M3U file
    * A URL for the schedule, preferrably as an XMLTV file
* `virtualmic` installed and working to provide desktop audio to the stream
* PDM installed to manage dependencies

### How to do this

With all the stuff above installed, do the following:

1. Run `pdm install` to install the virtual environment and dependencies
2. Rename `.env.example` to `.env` in the `src` directory
3. Fill out the `.env` file with the necessary details
4. Create a database in MySQL called `pydreamtv`
5. Use the SQL scripts to create the necessary tables
6. Change to the `src` directory
7. Run `pydreamtv/bot.py`
8. Wait for the channel and programme databases to fill
9. Go to a voice channel in Discord
10. Type `tv random` in chat
11. When the `mpv` window appears, stream the window to the voice chat
12. Swap the desktop audio to the virtual mic output

### Limitations

* Discord streaming audio is terrible. It uses the Opus codec and the audio quality is controlled by server boosts. Level 1 boosts can get 128Kbps quality
* There is a fallback channel which is used when a channel is offline, just pick a channel URL from the playlist file, preferrably one that is reliable
* The bot attempts to keep the `mpv` window open as much as possible so that Discord doesn't lose the window handle, but it can be hit and miss sometimes
* This script assumes that the categories from the channel playlists contain some country codes at the start
* The playlist imported does make some assumptions about the channel metadata format. YMMV.
