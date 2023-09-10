#!/usr/bin/env python3
"""
Use the mpv library to control the output

Playlist notes
==============

xui-id: 
tvg-id->tv/channel@id or tv/programme@channel
tvg-name: Channel name
tvg-logo: URL for the logo
group-title: First part is a group in double quotes
    About 212 categories
    Some prefixed with country codes
    
?: remainder of the line is a duplicate of the tvg-name


Build a bot that listens to commands

/tv search xyz <- Search for a station or program


"""


import mpv
from time import sleep

player = mpv.MPV()
player.play("http://neczmabfa.to:80/play/Mb_As84PELDIm3i5VJ_8nJiRif9MkF8lvTpXiBjQ5TM5sbhQXiNr8gHdV0FOxn6-/ts")
sleep(10)

del player


