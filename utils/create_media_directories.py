import pathlib


def create_directories() -> None:
    base_directory = pathlib.Path("media")

    if not base_directory.exists():
        base_directory.mkdir()

    subdirectories = ["video", "audio", "combined"]

    for subdirectory in subdirectories:
        subdirectory_path = base_directory / subdirectory
        if not subdirectory_path.exists():
            subdirectory_path.mkdir()
