from pytube import YouTube

import unicodedata
import re

import os
import time

import uuid

def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD',
                                      value).encode('ascii',
                                                    'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


# https://www.youtube.com/watch?v=sFIbcgHrGSg

try:
    while True:
        print("* "*10 + "YouTube Video Converter" + " *"*10)
        link = input("Enter video link > ")
        print("* "*10 + "Video Format" + " *"*10)
        print("1. MP3")
        print("2. MP4")
        print("3. BOTH")
        format = input("Enter video format > ").lower()
        try:

            yt = YouTube(link)
            # print(yt.title)
            yt.title = slugify(yt.title)
            # yt.title = str(uuid.uuid4())
            
            if format == "1" or format == "mp3":
              yt.streams.first().download()
              os.rename(f'{yt.title}.3gpp', f'{yt.title}.mp3')
              print("MP3 downloaded")
            elif format == "2" or format == "mp4":
              yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()
              print("MP4 downloaded")
            elif format == "3" or format == "both":
              yt.streams.first().download()
              yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()
              os.rename(f'{yt.title}.3gpp', f'{yt.title}.mp3')
              print("MP3 and MP4 downloaded")
            else:
              print("Invalid format")
            
        except Exception as e:
            print(e)

except KeyboardInterrupt:
    pass
