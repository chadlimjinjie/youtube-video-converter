from pytube import YouTube

import unicodedata
import re

import os
import time

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
        link = input("Enter video link > ")
        try:
            yt = YouTube(link)

            yt.title = slugify(yt.title)
            yt.streams.first().download()
            yt.streams.filter(progressive=True, file_extension='mp4').order_by(
                'resolution').desc().first().download()
            time.sleep(1)

            os.rename(f'{yt.title}.3gpp', f'{yt.title}.mp3')

            print("MP4 & MP3 downloaded")
        except Exception as e:
            print(e)

except KeyboardInterrupt:
    pass
