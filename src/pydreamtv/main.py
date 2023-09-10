#!/usr/bin/env python3
import os
import click
import requests
from pathlib import Path
from pydreamtv.playlist import Playlist
import mysql.connector
from pydreamtv.channel import Channel
from lxml import etree
from datetime import datetime
from dotenv import load_dotenv
"""
Load the playlist
Load the XMLTV schedule
Store it all in a database
Parse Discord bot commands
    /tv search program
    /tv categories
    /tv channel ID
    /tv guide
Support two tuners
Use the MPV library
Screen share the MPV screen in Discord
"""


load_dotenv()


PLAYLIST = os.getenv("PLAYLIST")
XMLTV = os.getenv("XMLTV")


playlist = Playlist(Path("playlist.m3u"))


def dbq(field: str) -> str:
    return field.replace("'", "''")


@click.command()
def main():
    connection = mysql.connector.connect(
        user="root",
        password="zappa",
        host="127.0.0.1",
        database="pydreamtv"
    )

    cursor = connection.cursor()

    cursor.execute("TRUNCATE TABLE channels")
    connection.commit()

    # cursor.execute("SELECT xui_id, tvg_id, tvg_name, tvg_logo, group_title, url, created_at FROM channels")
    # print(f"Current row count: {cursor.rowcount}")
    # for (xui_id, tvg_id, tvg_name, tvg_logo, group_title, url, created_at) in cursor:
    #     print(f"xui_id: {xui_id}")

    click.echo("Fetching playlist...", nl=False)

    response = requests.get(PLAYLIST)
    if response.status_code != 200:
        raise Exception(f"Cannot download playlist: {response.content}")

    click.echo("done.")
    click.echo("Adding channels to database...", nl=False)

    channel = None

    for line in response.content.splitlines():
        if line.startswith(b'#EXTINF:'):
            # This line contains information about the video duration, skip it
            channel = Channel.from_playlist_line(line.decode())
            continue
        elif line.startswith(b'#') or line.strip() == "":
            continue  # This line is a comment or metadata, skip it
        else:
            # This line contains the video file path
            if channel:
                channel.url = line.strip().decode()
                cursor.execute(
                    "INSERT INTO channels (xui_id, tvg_id, tvg_name, tvg_logo, group_title, url) "
                    f"VALUES ({channel.xui_id}, '{channel.tvg_id}', '{dbq(channel.tvg_name)}', '{channel.tvg_logo}', '{dbq(channel.group_title)}', '{dbq(channel.url)}')"
                )
                channel = None

    connection.commit()

    click.echo("done.")

    if not Path("xmltv.xml").exists():
        click.echo("Fetch XMLTV...", nl=False)
        response = requests.get(XMLTV)
        if response.status_code != 200:
            raise Exception(f"Cannot download XMLTV: {response.content}")

        click.echo("done.")
        click.echo("Adding programmes to database...", nl=False)

        with open("xmltv.xml", "w+b") as xmltv_handle:
            xmltv_handle.write(response.content)

        click.echo("done.")

    click.echo("Parsing XML...", nl=False)

    with open("xmltv.xml", "r+b") as xmltv_handle:
        root = etree.fromstring(xmltv_handle.read())

    click.echo("done.")
    click.echo("Adding XMLTV to database...", nl=False)

    for programme in root.xpath("/tv/programme"):
        title = ""
        description = ""
        for child in programme:
            if child.tag == "title" and child.text:
                title = child.text
            elif child.tag == "desc" and child.text:
                description = child.text

        try:
            # Some descriptions are beyond UTF-8 and don't get written
            start = datetime.strptime(programme.get("start"), "%Y%m%d%H%M%S %z")
            stop = datetime.strptime(programme.get("stop"), "%Y%m%d%H%M%S %z")

            cursor.execute(
                "INSERT INTO programmes (start, stop, start_timestamp, stop_timestamp, channel, title, description) "
                f"VALUES ('{start.isoformat()}', '{stop.isoformat()}', {programme.get('start_timestamp')}, {programme.get('stop_timestamp')}, '{dbq(programme.get('channel'))}', '{dbq(title)}', '{dbq(description)}')"
            )
        except mysql.connector.errors.ProgrammingError:
            pass

    connection.commit()

    click.echo("done.")

    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()
