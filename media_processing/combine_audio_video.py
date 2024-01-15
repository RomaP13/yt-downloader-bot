from typing import Dict

import ffmpeg


def combine(paths: Dict[str, str]) -> None:
    video = ffmpeg.input(paths["video"])
    audio = ffmpeg.input(paths["audio"])
    out = ffmpeg.output(
        video, audio, paths["combined"],
        vcodec="libx264", acodec="aac",
        strict="experimental"
    )
    out.run(overwrite_output=True)
