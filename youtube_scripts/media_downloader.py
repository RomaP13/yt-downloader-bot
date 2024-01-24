import pathlib
import logging

from pytube.streams import Stream


class FileSizeLimitExceededError(Exception):
    pass


def check_file_size_limit(file_path: str, max_size_MB: int = 50) -> None:
    # Get the file size in bytes
    file_size_bytes = pathlib.Path(file_path).stat().st_size

    # Convert bytes to megabytes
    file_size_MB = file_size_bytes / (1024 * 1024)

    if file_size_MB >= max_size_MB:
        raise FileSizeLimitExceededError(f"File size ({file_size_MB:.2f} MB) exceeds the limit of {max_size_MB} MB.")


def download_file(path: str, stream: Stream) -> bool:
    try:
        logging.info("Downloading file...")
        parts = path.split("/")
        stream.download(
            output_path=f"{parts[0]}/{parts[1]}/",
            filename=parts[-1]
        )

        check_file_size_limit(path)

        return True  # Return True if the download is successful
    except FileSizeLimitExceededError as e:
        logging.exception("Error downloading file '%s': %s", path, e)
        return False  # Return False if the file size exceeds the limit
    except Exception as e:
        logging.exception("Error downloading file '%s': %s", path, e)
        return False  # Return False for other errors
