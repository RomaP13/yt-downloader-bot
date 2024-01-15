from pytube import YouTube


def get_title(url: str) -> str:
    title = YouTube(url).title
    return title
