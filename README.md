# yt-downloader-bot
This project is a Python-based Telegram bot designed for convenient downloads of YouTube videos and music.

![app-preview](preview.png)

## Installation
1. Clone this repository:
```
   git clone https://github.com/RomaP13/yt-downloader-bot
   cd yt-downloader-bot
```

2. Create a file named ".env" and add your key in this file.
```
BOT_TOKEN = <TOKEN>
```

3. Install the required Python packages:
```
pip install -r requirements.txt
```

4. Run the bot:
```
python -O bot.py
```

## Limitations
Note: The bot has a file size limit of 50 MB for uploads. If you require larger files, consider running your own local server using the Local Bot API Server, allowing you to send files up to 2 GB in size.

## License
[MIT](https://choosealicense.com/licenses/mit/)
