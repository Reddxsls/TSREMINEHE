# ShowDownloader

## Introduction
Scripts for automatically downloading shows from official sites. Currently supports **PBS Kids** and **Disney Now**.

Note: For **Disney Now** the quality is limited since I have limited space on my server. For full quality delete the following line from `disneynowdl.py`

``` python
'format': '[tbr<=2199]',
```

Each episode will be around a gig.

## Requirements
- python3
- python3-pip
- pip install yt-dlp HTMLParser requests

## How to Use
Edit the `show_downloader.conf` file by placing a 1 next to the shows you DO want to download and a 0 next to those you do NOT. First clone has all values set to 0

This is a current updated list of all shows available as of 17 Sept 2021.

Then simply run:
```
python3 show_downloader.py
```

Throw it in a cron to have it run each night and you won't miss anything.

## Known Issues
- No subtitle support: I have not figured out how to get the subtitles for these shows yet
