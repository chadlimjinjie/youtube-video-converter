from tkinter import *
from tkinter import ttk
from pytube import YouTube

import unicodedata
import re

import os

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


def download():
    try:

        link = link_var.get()
        format = format_var.get()
        print(link)
        print(format)

        yt = YouTube(link)
        # print(yt.title)
        yt.title = slugify(yt.title)
        # yt.title = str(uuid.uuid4())

        if format == "1" or format == "mp3":
            yt.streams.first().download()
            os.rename(f'{yt.title}.3gpp', f'{yt.title}.mp3')
            print("MP3 downloaded")
        elif format == "2" or format == "mp4":
            yt.streams.filter(progressive=True, file_extension='mp4').order_by(
                'resolution').desc().first().download()
            print("MP4 downloaded")
        elif format == "3" or format == "both":
            yt.streams.first().download()
            yt.streams.filter(progressive=True, file_extension='mp4').order_by(
                'resolution').desc().first().download()
            os.rename(f'{yt.title}.3gpp', f'{yt.title}.mp3')
            print("MP3 and MP4 downloaded")
        else:
            print("Invalid format")

    except Exception as e:
        print(e)
    link_var.set("")


root = Tk()
root.title("YouTube Video Converter")

frm = ttk.Frame(root, padding=10)
link_var = StringVar(frm)
format_var = StringVar(frm, "1")
frm.grid()
ttk.Entry(frm, textvariable=link_var).grid(column=0, row=0)
ttk.Button(frm, text="Download", command=download).grid(column=2, row=0)

ttk.Radiobutton(frm, text="MP3", value="1", variable=format_var).grid(column=0, row=1)
ttk.Radiobutton(frm, text="MP4", value="2", variable=format_var).grid(column=1, row=1)
ttk.Radiobutton(frm, text="BOTH", value="3", variable=format_var).grid(column=2, row=1)

# ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=2)

root.mainloop()
