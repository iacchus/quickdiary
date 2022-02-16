#!/usr/bin/env python

#from os.path import expanduser
#from os import getenv
import os
from hashlib import sha256
import datetime
import subprocess
import click

from . import DATETIME

#
# ENVIRONMENT NAME constants
#
ENVNAME_DIARY_FILENAME="QUICKDIARY_FILENAME"
ENVNAME_DATE_FORMAT="QUICKDIARY_DATE_FORMAT"
ENVNAME_TIME_FORMAT="QUICKDIARY_TIME_FORMAT"
ENVNAME_EDITOR="QUICKDIARY_EDITOR"
ENVNAME_EDITOR_PARAMS="QUICKDIARY_EDITOR_PARAMS"

#
# DEFAULT constants
#
DEFAULT_DIARY_FILENAME = "~/diary.quickdiary"

DAY_OF_MONTH = str(int(DATETIME.strftime("%d")))  # without the zero padding
DEFAULT_DATE_FORMAT = "%A, %B {day_of_month}, %Y"

DEFAULT_TIME_FORMAT = "%H:%M:%S: "

DEFAULT_EDITOR = os.getenv('EDITOR')
DEFAULT_EDITOR_PARAMS = "+norm GA"  # this is for vim: go to the end of the file


#
# PRESET constants
#
PRESET_DIARY_FILENAME = os.getenv(key=ENVNAME_DIARY_FILENAME,
                                  default=DEFAULT_DIARY_FILENAME)
PRESET_DATE_FORMAT = os.getenv(key=ENVNAME_DATE_FORMAT,
                                  default=DEFAULT_DATE_FORMAT)
PRESET_TIME_FORMAT = os.getenv(key=ENVNAME_TIME_FORMAT,
                                  default=DEFAULT_TIME_FORMAT)
PRESET_EDITOR = os.getenv(key=ENVNAME_EDITOR,
                                  default=DEFAULT_EDITOR)
PRESET_EDITOR_PARAMS = os.getenv(key=ENVNAME_EDITOR_PARAMS,
                                  default=DEFAULT_EDITOR_PARAMS)


@click.command()
@click.option("--file", "-f", "filename", type=str,
              default=PRESET_DIARY_FILENAME, metavar="<filename>",
              help="File to add entry")
@click.option("--prompt", "-p", "prompt", is_flag=True,
              help="Shows a prompt to add entry, instead of opening the text editor")
def cli(filename, prompt):

    # `day_of_month` is the day of the month without the zero padding
    day_of_month = str(int(DATETIME.strftime("%d")))

    # `date` is like "Wednesday, February 16, 2022" (before the first entry
    #     of the day)
    date = str(DATETIME.strftime(PRESET_DATE_FORMAT
                                 .format(day_of_month=day_of_month)))
    # `time` is like "18:51:22: " (before each entry)
    time = str(DATETIME.strftime(PRESET_TIME_FORMAT))

    # `date_hash` is the SHASUM256(date), used as a signature so a current date
    #     entered by the user on a single line don't gets confused as a
    #     timestamp marking
    date_hash = sha256(date.encode("utf-8")).hexdigest()

    # `date_hash_string` is the string which will be added each new day, only
    #     once a day (unless you change `date` format)
    date_hash_string = "{date} [{date_hash}]".format(date=date,
                                                 date_hash=date_hash)

    filename_path = os.path.expanduser(filename)

    diary_file_exists = os.path.exists(filename_path)

    # will we use our embedded prompt for the entry or, intead, the user is
    #     going to use his $EDITOR?
    if prompt:
        text = click.prompt('{}:'.format(time))
    else:
        text = None

    add_date = bool(True)

    if diary_file_exists:  # then check if the current date was already added,
                           #     if not we will add it later
                           #     (`date_hash_string`)
        with open(os.path.expanduser(filename_path), 'r') as diary_file:
            for line in diary_file:
                if date_hash_string == line.strip():
                    add_date = False
    else:
        print("File '{}' doesn't exist. Creating...".format(filename_path))

    with open(filename_path, 'a+') as diary_file:
        click.echo("Writing to file '{filename_path}'"
                   .format(filename_path=filename_path))

        if add_date:  # is this the first entry of the day? then add the date
            diary_file.write ("{date_hash_string}"
                              .format(date_hash_string=date_hash_string))

        # add entry "HH:MM:SS: "
        diary_file.write ("\n\n{time}".format(time=time))

        if text:  # text was entered by prompt
            diary_file.write(text)

    if not text:  # then text will be entered manually via PRESET_EDITOR
                  #     which is shell's `$EDITOR` or our `ENVNAME_EDITOR` env
        subprocess.call([PRESET_EDITOR, PRESET_EDITOR_PARAMS, filename_path])


if __name__ == "__main__":
    cli()
