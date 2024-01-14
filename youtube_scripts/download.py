from pytube.streams import Stream


async def download_files(
    v_path: str,
    a_path: str,
    v_stream: Stream,
    a_stream: Stream
) -> None:
    if v_stream:
        parts = v_path.split("/")
        v_stream.download(
            output_path=f"{parts[0]}/{parts[1]}/",
            filename=parts[-1]
        )

    if a_stream:
        parts = a_path.split("/")
        a_stream.download(
            output_path=f"{parts[0]}/{parts[1]}/",
            filename=parts[-1]
        )
