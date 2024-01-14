from typing import Dict

from pytube import YouTube
from pytube.streams import Stream
from pytube.query import StreamQuery


async def get_streams(url: str) -> StreamQuery:
    yt = YouTube(url)
    streams = yt.streams.filter(file_extension="mp4")
    return streams


async def get_video_streams(streams: StreamQuery, only_video: bool) -> Dict[str, Stream]:
    video = streams.filter(type="video", file_extension="mp4").order_by("resolution")
    video_streams_by_res = {}

    # Since adaptive streams come first, all
    # possible adaptive streams will be included
    for stream in video:
        print(f"WWWWWWW: {stream}\nWWWWWWW: {only_video}\nWWWWWWW: {stream.is_adaptive}")
        if (only_video and stream.is_adaptive) or (not only_video and stream.resolution not in video_streams_by_res):
            video_streams_by_res[stream.resolution] = stream

    return video_streams_by_res


async def get_audio_stream(streams: StreamQuery) -> Stream:
    audio = streams.get_audio_only()
    return audio
