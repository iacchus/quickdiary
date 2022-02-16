#!/usr/bin/env python

from os.path import expanduser
from os import getenv
from hashlib import sha256
import datetime

FILENAME = expanduser("~/diary.quickdiary")

DATETIME = datetime.datetime.now()
#DATE = str(DATETIME.date())
#TIMEMS = str(DATETIME.time())
DAY_OF_MONTH = str(int(DATETIME.strftime("%d")))  # without the zero padding
DATE = str(DATETIME.strftime("%A, %B {day_of_month}, %Y".format(day_of_month=DAY_OF_MONTH)))
TIME = str(DATETIME.strftime("%H:%M:%S"))

DATE_HASH = sha256(DATE).hexdigest()
DATE_HASH_STRING = "{date} {HASH}".format(date=DATE, hash=HASH)

EDITOR = os.getenv('EDITOR')
EDITOR_OPTIONS = "+norm G"  # go to the end of the file

add_date = true

def cli:
    with open(FILENAME) as diary_file:
        for line in diary_file:
            if line.strip() == DATE_HASH_STRING:
                add_date = false

        if add_date:
            diary_file.write ("\n\n{date_hash_string}\n\n"
                              .format(date_hash_string=DATE_HASH_STRING))

        diary_file.write ("\n\n{time}: ".format(time=TIME))

subprocess.call([EDITOR, EDITOR_OPTIONS, FILENAME])


