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
ENVNAME_PAGER="QUICKDIARY_PAGER"
ENVNAME_PAGER_PARAMS="QUICKDIARY_PAGER_PARAMS"

#
# DEFAULT constants
#
DEFAULT_DIARY_FILENAME = "~/diary.quickdiary"

DAY_OF_MONTH = str(int(DATETIME.strftime("%d")))  # without the zero padding
DEFAULT_DATE_FORMAT = "%A, %B {day_of_month}, %Y"

DEFAULT_TIME_FORMAT = "%H:%M:%S"

DEFAULT_EDITOR = os.getenv('EDITOR')
DEFAULT_EDITOR_PARAMS = "+norm GA"  # this is for vim: go to the end of the file


DEFAULT_PAGER = os.getenv('PAGER')
DEFAULT_PAGER_PARAMS = "+norm GA"  # this is for vim: go to the end of the file

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
PRESET_PAGER = os.getenv(key=ENVNAME_PAGER,
                         default=DEFAULT_PAGER)
PRESET_PAGER_PARAMS = os.getenv(key=ENVNAME_PAGER_PARAMS,
                                default=DEFAULT_PAGER_PARAMS)

# `day_of_month` is the day of the month without the zero padding
DAY_OF_MONTH = str(int(DATETIME.strftime("%d")))

# `date` is like "Wednesday, February 16, 2022" (before the first entry
#     of the day)
DATE = str(DATETIME.strftime(PRESET_DATE_FORMAT
                             .format(day_of_month=DAY_OF_MONTH)))
# `time` is like "18:51:22: " (before each entry)
TIME = str(DATETIME.strftime(PRESET_TIME_FORMAT))

# `date_hash` is the SHASUM256(date), used as a signature so a current date
#     entered by the user on a single line don't gets confused as a
#     timestamp marking
DATE_HASH = sha256(DATE.encode("utf-8")).hexdigest()

# `date_hash_string` is the string which will be added each new day, only
#     once a day (unless you change `date` format)
DATE_HASH_STRING = "{date} [{date_hash}]".format(date=DATE,
                                             date_hash=DATE_HASH)

def already_has_current_date_entry(filename):
    """Looks in file for a line containing `DATE_HASH_STRING`
    """

    has_date = False

    with open(os.path.expanduser(filename), 'r') as diary_file:
        for line in diary_file:
            if DATE_HASH_STRING == line.strip():
                has_date = True

    return has_date

# ┌────────────┐
# │ quickdiary │
# └────────────┘

@click.group()
def quickdiary():
    pass

# ┌───────┐
# │ write │
# └───────┘

write_epilog = "Writes to diary file using $EDITOR or ${}"\
               .format(ENVNAME_EDITOR)
@quickdiary.command(epilog=write_epilog)
@click.option("--file", "-f", "filename", type=str,
              default=PRESET_DIARY_FILENAME, metavar="<filename>",
              help="File to add entry")
def write(filename):
    """Writes to diary using configured editor.
    """

    filename_path = os.path.expanduser(filename)

    diary_file_exists = os.path.exists(filename_path)

    if diary_file_exists:
        has_date = already_has_current_date_entry(filename_path)
    else:
        has_date = False
        click.echo("Creating new file '{}'...".format(filename_path))

    with open(filename_path, 'a+') as diary_file:
        click.echo("Writing to file '{filename_path}'"
                   .format(filename_path=filename_path))

        if not has_date:  # is this the first entry of the day?
                          #     then add the date, `DATE_HASH_STRING`
            diary_file.write ("\n\n{date_hash_string}"
                              .format(date_hash_string=DATE_HASH_STRING))

        # add entry "HH:MM:SS: "
        diary_file.write ("\n\n{time}: ".format(time=TIME))

    subprocess.call([PRESET_EDITOR, PRESET_EDITOR_PARAMS, filename_path])

# ┌────────┐
# │ prompt │
# └────────┘

prompt_epilog = "Prompts for the text to add to the diary."
@quickdiary.command(epilog=prompt_epilog)
@click.option("--file", "-f", "filename", type=str,
              default=PRESET_DIARY_FILENAME, metavar="<filename>",
              help="File to add entry")
@click.option("--text", "-t", "text", type=str,
              prompt="{date}\n{time}".format(date=DATE, time=TIME),
              metavar="<text>", help="Text entry to write to the diary")
def prompt(filename, text):
    """Prompts for the entry to be added to the diary.
    """

    filename_path = os.path.expanduser(filename)

    diary_file_exists = os.path.exists(filename_path)

    #text = click.prompt('{}:'.format(TIME))

    if diary_file_exists:
        has_date = already_has_current_date_entry(filename_path)
    else:
        has_date = False
        click.echo("Creating new file '{}'...".format(filename_path))

    with open(filename_path, 'a+') as diary_file:
        click.echo("Writing to file '{filename_path}'"
                   .format(filename_path=filename_path))

        if not has_date:  # is this the first entry of the day?
                          #     then add the date, `DATE_HASH_STRING`
            diary_file.write ("\n\n{date_hash_string}"
                              .format(date_hash_string=DATE_HASH_STRING))

        # add entry "HH:MM:SS: " and the text
        diary_file.write ("\n\n{time}: {text}".format(time=TIME, text=text))

# ┌──────┐
# │ edit │
# └──────┘

edit_epilog = "Opens the diary file in the configured text editor."
@quickdiary.command(epilog=edit_epilog)
@click.option("--file", "-f", "filename", type=str,
              default=PRESET_DIARY_FILENAME, metavar="<filename>",
              help="File to add entry")
def edit(filename):
    """Opens the diary file in $EDITOR or $QUICKDIARY_EDITOR.
    """

    filename_path = os.path.expanduser(filename)

    diary_file_exists = os.path.exists(filename_path)

    if not diary_file_exists:
        click.echo("File '{}' doesn't exist.".format(filename_path))
    else:
        subprocess.call([PRESET_EDITOR, PRESET_EDITOR_PARAMS, filename_path])

# ┌───────┐
# │ pager │
# └───────┘

pager_epilog = "Opens the diary file in the configured environment pager."
@quickdiary.command(epilog=pager_epilog)
@click.option("--file", "-f", "filename", type=str,
              default=PRESET_DIARY_FILENAME, metavar="<filename>",
              help="File to add entry")
def pager(filename):
    """Opens the diary file in $PAGER or $QUICKDIARY_PAGER.
    """

    filename_path = os.path.expanduser(filename)

    diary_file_exists = os.path.exists(filename_path)

    if not diary_file_exists:
        click.echo("File '{}' doesn't exist.".format(filename_path))
    else:
        subprocess.call([PRESET_PAGER, PRESET_PAGER_PARAMS, filename_path])

# ┌─────┐
# │ cat │
# └─────┘

cat_epilog = "Prints the diary file to stdout."
@quickdiary.command(epilog=cat_epilog)
@click.option("--file", "-f", "filename", type=str,
              default=PRESET_DIARY_FILENAME, metavar="<filename>",
              help="File to add entry")
def cat(filename):
    """Prints the diary file to stdout.
    """

    filename_path = os.path.expanduser(filename)

    diary_file_exists = os.path.exists(filename_path)

    if not diary_file_exists:
        click.echo("File '{}' doesn't exist.".format(filename_path))
    else:
        with open(filename_path, 'r') as diary_file:
            for line in diary_file:
                click.echo(line, nl=False)


if __name__ == "__main__":
    quickdiary()
