# pydreamtv

## Stream IPTV to Discord.

Beware, this is in early stages but it does work. It needs a bit to get it going, but if you understand IPTV providers and how Discord voice chat works then it should make sense. The instructions are brief and makes assumptions that you understand the individual parts rather than going into details on how each stage works.

This janky bot does the following:

* Listens to commands on a server for `tv` commands
* Controls an instance of `mpv` via these commands
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

### How to do this

With all the stuff above installed, do the following:

1. Rename `.env.example` to `.env` in the `src` directory
2. Fill out the `.env` file with the necessary details
3. Create a database in MySQL called `pydreamtv`
4. Use the SQL scripts to create the necessary tables
5. Change to the `src` directory
6. Run `pydreamtv/bot.py`
7. Wait for the channel and programme databases to fill
8. Go to a voice channel in Discord
9. Type `tv random` in chat
10. When the `mpv` window appears, stream the window to the voice chat
11. Swap the desktop audio to the virtual mic output
