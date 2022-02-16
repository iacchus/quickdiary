#!/usr/bin/env python

#from os.path import expanduser
#from os import getenv
import os
from hashlib import sha256
import datetime
import subprocess
import click

# ENVIRONMENT NAME constants
ENVNAME_DIARY_FILENAME="QUICKDIARY_FILENAME"

# DEFAULT constants
DEFAULT_DIARY_FILENAME = os.path.expanduser("~/diary.quickdiary")

# PRESET constants
PRESET_DIARY_FILENAME = os.getenv(key=ENVNAME_DIARY_FILENAME,
                                  default=DEFAULT_DIARY_FILENAME)

#DIARY_FILE_EXISTS = os.path.exists(DIARY_FILENAME)

DATETIME = datetime.datetime.now()
#DATE = str(DATETIME.date())
#TIMEMS = str(DATETIME.time())
DAY_OF_MONTH = str(int(DATETIME.strftime("%d")))  # without the zero padding
DATE = str(DATETIME.strftime("%A, %B {day_of_month}, %Y"
           .format(day_of_month=DAY_OF_MONTH)))
TIME = str(DATETIME.strftime("%H:%M:%S"))

DATE_HASH = sha256(DATE.encode("utf-8")).hexdigest()
DATE_HASH_STRING = "{date} [{date_hash}]".format(date=DATE,
                                                 date_hash=DATE_HASH)

EDITOR = os.getenv('EDITOR')
EDITOR_OPTIONS = "+norm GA"  # go to the end of the file


#if DIARY_FILE_EXISTS:  # then check if the current date was already added
#    with open(DIARY_FILENAME, 'r') as diary_file:
#        for line in diary_file:
#            if DATE_HASH_STRING == line.strip():
#                add_date = False

@click.command()
@click.option("--file", "-f", "filename", type=str, default=PRESET_DIARY_FILENAME)
@click.option("--text", "-t", "text", type=str, prompt=True, default='')
def cli(filename, text):

    diary_file_exists = os.path.exists(filename)

    add_date = bool(True)

    if diary_file_exists:  # then check if the current date was already added
        with open(filename, 'r') as diary_file:
            for line in diary_file:
                if DATE_HASH_STRING == line.strip():
                    add_date = False

    with open(filename, 'a') as diary_file:
        click.echo("Writing to file '{filename}'"
                   .format(filename=filename))

        if add_date:
            diary_file.write ("{date_hash_string}"
                              .format(date_hash_string=DATE_HASH_STRING))

        diary_file.write ("\n\n{time}: ".format(time=TIME))

    subprocess.call([EDITOR, EDITOR_OPTIONS, filename])


if __name__ == "__main__":
    cli()
