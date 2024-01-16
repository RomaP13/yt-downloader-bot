import logging

from typing import Dict

from pytube import YouTube
from pytube.streams import Stream
from pytube.query import StreamQuery


def get_streams(url: str) -> StreamQuery | None:
    try:
        yt = YouTube(url)
        streams = yt.streams.filter(file_extension="mp4")
        return streams
    except TypeError as e:
        logging.exception("An error occurred in get_streams: %s. Url: %s",
                          str(e), url)

    return None


def get_video_streams(
    streams: StreamQuery, only_video: bool
) -> Dict[str, Stream]:
    video = streams.filter(type="video",
                           file_extension="mp4").order_by("resolution")

    video_streams_by_res = {}
    for stream in video:
        if (only_video and stream.is_adaptive) or (
            not only_video and stream.resolution not in video_streams_by_res
        ):
            video_streams_by_res[stream.resolution] = stream

    return video_streams_by_res


def get_audio_stream(streams: StreamQuery) -> Stream:
    audio = streams.get_audio_only()
    return audio
