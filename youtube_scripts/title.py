from pytube import YouTube


async def get_title(url: str) -> str:
    title = YouTube(url).title
    print(f"TITLE: {title}")
    return title
