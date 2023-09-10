import re
from dataclasses import dataclass


PATTERN = re.compile(
    r"#EXTINF:.*\s*xui-id=\"(?P<xui_id>\d*)\"\s*tvg-id=\"(?P<tvg_id>.*?)\""
    r"\s*tvg-name=\"(?P<tvg_name>.*?)\"\s*tvg-logo=\"(?P<tvg_logo>.*?)\"\s*"
    r"group-title=\"(?P<group_title>.*?)\""
)


@dataclass
class Channel:
    """
    xui-id: integer
    tvg-id->tv/channel@id or tv/programme@channel
    tvg-name: Channel name
    tvg-logo: URL for the logo
    group-title: First part is a group in double quotes
        About 212 categories
        Some prefixed with country codes

    remainder of the line is a duplicate of the tvg-name
    """
    xui_id: int
    tvg_id: str
    tvg_name: str
    tvg_logo: str
    group_title: str
    prefix: str
    url: str = None

    @classmethod
    def from_playlist_line(cls, line: str) -> "Channel":
        """
        #EXTINF:-1 xui-id="4075" tvg-id="bbc1.uk" tvg-name="UK: BBC One FHD" tvg-logo="http://neczmabfa.to:80/images/75de4fb3b8850cb15181ab91a55ef4c5.png" group-title="UK: | Entertainment",UK: BBC One FHD
        """
        matches = PATTERN.match(line)
        if matches:
            prefix, _, _ = matches["group_title"].partition(": |")
            return cls(
                xui_id=int(matches["xui_id"]),
                tvg_id=matches["tvg_id"],
                tvg_name=matches["tvg_name"],
                tvg_logo=matches["tvg_logo"],
                group_title=matches["group_title"],
                prefix=prefix
            )
        
        return None
