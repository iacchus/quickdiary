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

#
# DEFAULT constants
#
#DEFAULT_DIARY_FILENAME = os.path.expanduser("~/diary.quickdiary")
DEFAULT_DIARY_FILENAME = "~/diary.quickdiary"

DAY_OF_MONTH = str(int(DATETIME.strftime("%d")))  # without the zero padding
DEFAULT_DATE_FORMAT = "%A, %B {day_of_month}, %Y"

#DEFAULT_TIME_FORMAT = str(DATETIME.strftime("%H:%M:%S"))
DEFAULT_TIME_FORMAT = "%H:%M:%S: "

#
# PRESET constants
#
PRESET_DIARY_FILENAME = os.getenv(key=ENVNAME_DIARY_FILENAME,
                                  default=DEFAULT_DIARY_FILENAME)
PRESET_DATE_FORMAT = os.getenv(key=ENVNAME_DATE_FORMAT,
                                  default=DEFAULT_DATE_FORMAT)
PRESET_TIME_FORMAT = os.getenv(key=ENVNAME_TIME_FORMAT,
                                  default=DEFAULT_TIME_FORMAT)


#DIARY_FILE_EXISTS = os.path.exists(DIARY_FILENAME)

#DATETIME = datetime.datetime.now()
#DATE = str(DATETIME.date())
#TIMEMS = str(DATETIME.time())
#DAY_OF_MONTH = str(int(DATETIME.strftime("%d")))  # without the zero padding

#DATE = str(DATETIME.strftime("%A, %B {day_of_month}, %Y"
#           .format(day_of_month=DAY_OF_MONTH)))
#TIME = str(DATETIME.strftime("%H:%M:%S"))
#DATE = str(DATETIME.strftime(PRESET_DATE_FORMAT))
#TIME = str(DATETIME.strftime(PRESET_TIME_FORMAT))

#DATE_HASH = sha256(DATE.encode("utf-8")).hexdigest()
#DATE_HASH_STRING = "{date} [{date_hash}]".format(date=DATE,
#                                                 date_hash=DATE_HASH)

EDITOR = os.getenv('EDITOR')
EDITOR_OPTIONS = "+norm GA"  # go to the end of the file


#if DIARY_FILE_EXISTS:  # then check if the current date was already added
#    with open(DIARY_FILENAME, 'r') as diary_file:
#        for line in diary_file:
#            if DATE_HASH_STRING == line.strip():
#                add_date = False

@click.command()
@click.option("--file", "-f", "filename", type=str,
              default=PRESET_DIARY_FILENAME)
@click.option("--text", "-t", "text", is_flag=True)
def cli(filename, text):

    day_of_month = str(int(DATETIME.strftime("%d")))  # without the 0 padding
    date = str(DATETIME.strftime(PRESET_DATE_FORMAT
                                 .format(day_of_month=day_of_month)))
    time = str(DATETIME.strftime(PRESET_TIME_FORMAT))

    date_hash = sha256(date.encode("utf-8")).hexdigest()
    date_hash_string = "{date} [{date_hash}]".format(date=date,
                                                 date_hash=date_hash)

    filename_path = os.path.expanduser(filename)

    diary_file_exists = os.path.exists(filename_path)

    add_date = bool(True)

    if diary_file_exists:  # then check if the current date was already added
        with open(os.path.expanduser(filename_path), 'r') as diary_file:
            for line in diary_file:
                if date_hash_string == line.strip():
                    add_date = False
    print("File '{}' doesn't exist. Creating...".format(filename_path))
    with open(filename_path, 'a+') as diary_file:
        click.echo("Writing to file '{filename_path}'"
                   .format(filename_path=filename_path))

        if add_date:
            diary_file.write ("{date_hash_string}"
                              .format(date_hash_string=date_hash_string))

        diary_file.write ("\n\n{time}".format(time=time))

    subprocess.call([EDITOR, EDITOR_OPTIONS, filename_path])


if __name__ == "__main__":
    cli()
