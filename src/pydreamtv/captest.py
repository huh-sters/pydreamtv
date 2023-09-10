import os
import cv2
import requests
import re
from dataclasses import dataclass
from typing import List
import pyvirtualcam

os.system("sudo modprobe -r v4l2loopback")
os.system("sudo modprobe v4l2loopback")


PATTERN = re.compile(
    r"#EXTINF:.*\s*xui-id=\"(?P<xui_id>\d*)\"\s*tvg-id=\"(?P<tvg_id>.*?)\""
    r"\s*tvg-name=\"(?P<tvg_name>.*?)\"\s*tvg-logo=\"(?P<tvg_logo>.*?)\"\s*"
    r"group-title=\"(?P<group_title>.*?)$"
)


@dataclass
class ChannelMetadata:
    """
    #EXTINF:-1
    xui-id="4075"
    tvg-id="bbc1.uk"
    tvg-name="UK: BBC One FHD"
    tvg-logo="http://neczmabfa.to:80/images/75de4fb3b8850cb15181ab91a55ef4c5.png"
    group-title="UK: | Entertainment",UK: BBC One FHD"
    """
    xui_id: str
    tvg_id: str
    tvg_name: str
    tvg_logo: str
    group_title: str
    url: str = ""

    @classmethod
    def from_m3u_metadata(cls, metaline: str):
        matches = PATTERN.match(metaline)
        if matches:
            return cls(**matches.groupdict())
        
        return None


PLAYLIST = os.getenv("PLAYLIST")

def read_playlist(playlist: str) -> List[ChannelMetadata]:
    response = requests.get(playlist)

    if response.status_code != 200:
        print("Could not open M3U file")
        return []

    with open("playlist.m3u", "w") as playlist_handle:
        playlist_handle.write(response.content.decode("utf-8"))

    playlist_lines = response.content.decode("utf-8").split("\n")

    metadata = None
    channels = []

    # Loop through each line in the playlist
    for line in playlist_lines:
        if line.startswith('#EXTINF:'):
            # This line contains information about the video duration, skip it
            metadata = ChannelMetadata.from_m3u_metadata(line)
            continue
        elif line.startswith('#') or line.strip() == "":
            continue  # This line is a comment or metadata, skip it
        else:
            # This line contains the video file path
            if metadata:
                metadata.url = line.strip()
                channels.append(metadata)
                metadata = None

    return channels


read_playlist(PLAYLIST)

cap = None

# Open the video file
cap = cv2.VideoCapture("http://neczmabfa.to:80/play/Mb_As84PELDIm3i5VJ_8nJiRif9MkF8lvTpXiBjQ5TM5sbhQXiNr8gHdV0FOxn6-/ts")

if cap is not None:
    ret, frame = cap.read()  # Read a frame and get the dimensions
    height, width, _ = frame.shape
    fps = cap.get(cv2.CAP_PROP_FPS)
    with pyvirtualcam.Camera(
        width=width,
        height=height,
        fps=fps,
        fmt=pyvirtualcam.PixelFormat.BGR
    ) as cam:
        while True:
            ret, frame = cap.read()
    
            cam.send(frame)
            cam.sleep_until_next_frame()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    if cap is not None:
        cap.release()
