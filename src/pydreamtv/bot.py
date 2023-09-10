#!/usr/bin/env python3
import os
import click
import discord
import requests
from lxml import etree
from datetime import datetime
from discord.ext import commands
from discord.ext.commands.context import Context
import mysql.connector
from pydreamtv.channel import Channel
import mpv
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv
import asyncio


load_dotenv()


TOKEN = os.getenv("TOKEN")
GUILD = os.getenv("GUILD")
PLAYLIST = os.getenv("PLAYLIST")
XMLTV = os.getenv("XMLTV")
FALLBACK = os.getenv("FALLBACK")


current_overlay = None


def dbq(field: str) -> str:
    return field.replace("'", "''")


def connect() -> mysql.connector.connection:
    return mysql.connector.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host="127.0.0.1",
        database="pydreamtv"
    )


def play_with_description(url: str, message: str) -> None:
    global current_overlay
    if current_overlay:
        current_overlay.remove()

    font = ImageFont.truetype("NimbusSans-Regular.otf", 20)
    current_overlay = mpv.create_image_overlay()
    img = Image.new("RGBA", (400, 150), (255, 255, 255, 0))
    d = ImageDraw.Draw(img)
    d.text((10, 10), message, font=font, fill=(0, 255, 255, 128))
    current_overlay.update(img, pos=(10, 10))

    mpv.play(url)


def logit(loglevel, component, message):
    if loglevel in ["error", "fatal"] and (
        message.startswith("http: Stream ends prematurely")
    ):
        # Capture and play Dave
        play_with_description(FALLBACK, "Default channel, something went wrong...")

    if loglevel in ["error", "fatal"]:
        click.echo(f"{loglevel} | {component} | {message}")


# Define the bot's command prefix
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix="tv ")

randofun_mode = False

# MPV player
mpv = mpv.MPV(log_handler=logit)

# Event handler for when the bot is ready
@bot.event
async def on_ready() -> None:
    print(f'Logged in as {bot.user.name}')


@bot.command()
async def randofunon(ctx: Context) -> None:
    """Start the randofun mode. 1 Minute of channel play."""
    global randofun_mode
    await ctx.send(f"Channel fairy starting the fun.")

    randofun_mode = True
    while randofun_mode:
        connection = connect()
        cursor = connection.cursor()
        command = ctx.message.content
        command = command.replace("tv randofunon", "")
        if command != "":
            cursor.execute(f"SELECT * FROM channels WHERE country = '{command.strip()}' ORDER BY RAND() LIMIT 1")
        else:
            cursor.execute("SELECT * FROM channels WHERE group_title not like 'XXX%' ORDER BY RAND() LIMIT 1")

        row = cursor.fetchone()
        if row:
            play_with_description(row[5], f"(ID {row[0]}) {row[2]}")

        await ctx.send(f"Channel fairy randoming this bitch up (ID {row[0]}).")

        cursor.close()
        connection.close()
        await asyncio.sleep(60)


@bot.command()
async def randonext(ctx: Context) -> None:
    """Skip to the next track in randofun mode"""
    ctx.message.content = "tv random"
    await random(ctx)


@bot.command()
async def randofunoff(ctx: Context) -> None:
    """Stop the randofun mode"""
    global randofun_mode
    await ctx.send(f"Channel fairy stopping the fun.")
    randofun_mode = False


@bot.command()
async def search(ctx: Context) -> None:
    """Search for channels and programmes by a single word"""
    connection = connect()
    cursor = connection.cursor()
    command = ctx.message.content
    search_text = command.replace("tv search ", "").lower()
    cursor.execute(f"""
SELECT
	programmes.channel,
	programmes.title,
	programmes.description,
    channels.xui_id,
	channels.url
FROM
	programmes
	INNER JOIN channels ON
		programmes.channel = channels.tvg_id
WHERE 
	(	
		channel LIKE '%{search_text}%' OR
		title LIKE '%{search_text}%' OR
		description LIKE '%{search_text}%' OR
        group_title LIKE '%{search_text}%'
	) AND
	now() > start AND now() < stop LIMIT 10
""")
    class ButtonView(discord.ui.View):
        def __init__(self, url: str, description: str):
            super().__init__()
            self.url = url
            self.description = description

        @discord.ui.button(label="Watch")
        async def watch(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message(f"Watching {self.description}...")
            play_with_description(self.url, self.description)

    count = 0

    for row in cursor:
        embed = discord.Embed(
            title=f"(ID {row[3]}) {row[1]}",
            description=row[2],
            color=discord.Color.blue()
        )
        await ctx.send(
            embed=embed,
            view=ButtonView(row[4], f"(ID {row[3]}) {row[0]}")
        )
        count += 1

    cursor.close()
    connection.close()
    if count == 0:
        await ctx.send(f"No results found")


@bot.command()
async def refresh(ctx: Context) -> None:
    """Refresh the channels and XMLTV (very slow)"""
    ctx.send("Refreshing channels and programmes...")
    fill_db(True)
    ctx.send("Channels and programmes refreshed")


@bot.command()
async def id(ctx: Context) -> None:
    """Play a channel by ID"""
    connection = connect()
    cursor = connection.cursor()
    command = ctx.message.content
    xui_id = command.replace("tv id ", "").lower()
    cursor.execute(f"SELECT url, tvg_name FROM channels WHERE xui_id={xui_id}")
    row = cursor.fetchone()
    if row:
        play_with_description(row[0], f"(ID {xui_id}) {row[1]}")
        await ctx.send(f"{ctx.author.display_name} asked for channel ID {xui_id}")
    else:
        await ctx.send(f"Channel ID {xui_id} does not exist")

    cursor.close()
    connection.close()


@bot.command()
async def random(ctx: Context) -> None:
    """Play a random channel, add a country code to filter"""
    connection = connect()
    cursor = connection.cursor()
    command = ctx.message.content
    command = command.replace("tv random", "")
    if command != "":
        cursor.execute(f"SELECT * FROM channels WHERE country = '{command.strip()}' ORDER BY RAND() LIMIT 1")
    else:
        cursor.execute("SELECT * FROM channels WHERE group_title not like 'XXX%' ORDER BY RAND() LIMIT 1")

    row = cursor.fetchone()
    if row:
        play_with_description(row[5], f"(ID {row[0]}) {row[2]}")
        cursor.close()
        connection.close()
        await ctx.send(f"{ctx.author.display_name} asked for a random channel, channel fairy chose (ID {row[0]}) {row[2]}")
    else:
        await ctx.send(f"{ctx.author.display_name} asked for a random channel, but the channel fairy is too high on meth to figure anything out. Try again in a bit.")

@bot.command()
async def countries(ctx: Context) -> None:
    """List all countries available"""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("""SELECT DISTINCT country from channels ORDER BY country""")
    countries = []
    for row in cursor:
        countries.append(row[0])
    country_list = '\n'.join(countries)
    await ctx.send(f"Available countries:\n{country_list}")
    cursor.close()
    connection.close()


@bot.command()
async def categories(ctx: Context) -> None:
    """List all the available channel categories"""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT group_title FROM channels ORDER BY group_title")
    groups = ""
    for group_title in cursor:
        groups += f"{group_title[0]}\n"
    cursor.close()
    connection.close()

    await ctx.send(f"Available categories: {groups}"[:1900])


@bot.command()
async def stop(ctx: Context) -> None:
    """Stop a channel from playing"""
    mpv.stop()
    await ctx.send("Stopping TV session")


def fill_db(force: bool = False) -> None:
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("SELECT MAX(created_at) FROM channels")
    created_at = cursor.fetchone()

    if not created_at[0] or force:
        # Refresh the channel listing
        cursor.execute("TRUNCATE TABLE channels")
        connection.commit()

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
                        "INSERT INTO channels (xui_id, tvg_id, tvg_name, tvg_logo, group_title, url, country) "
                        f"VALUES ({channel.xui_id}, '{channel.tvg_id}', '{dbq(channel.tvg_name)}', '{channel.tvg_logo}', '{dbq(channel.group_title)}', '{dbq(channel.url)}', '{channel.prefix}')"
                    )
                    channel = None

        connection.commit()

        click.echo("done.")
    else:
        click.echo("Channels up to date")

    cursor.execute("SELECT MIN(created_at) as created_at FROM programmes")
    created_at = cursor.fetchone()

    # If the created_at is more than x days ago, refresh
    refresh = False

    if not created_at[0]:
        refresh = True
    else:
        created_at: datetime = created_at[0]
        difference = datetime.now() - created_at
        if difference.days > 7:
            refresh = True

    if refresh or force:
        click.echo("Schedule is more than 7 days old, fetching XMLTV...", nl=False)
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

        cursor.execute("TRUNCATE TABLE programmes")

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
    else:
        click.echo("TV Schedule up to date")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    # Fill the DB with stuff if necessary
    fill_db()

    # Run the bot with your token
    bot.run(TOKEN)
