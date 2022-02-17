# quickdiary 

| **Licensed with [GNU AGPLv3](https://github.com/iacchus/agplv3-resources/blob/master/LICENSE/LICENSE)**                                                                        |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [![agpl3](https://raw.githubusercontent.com/iacchus/agplv3-resources/main/LICENSE/agplv3-155x51.png)](https://github.com/iacchus/quickdiary/blob/main/LICENSE.txt) |

Simple command to add timestamped entries to a text file using `$EDITOR`.

[![Maintenance](https://img.shields.io/maintenance/yes/2022.svg?style=flat-square)](https://github.com/iacchus/quickdiary/issues/new?title=Is+quickdiary+still+maintained&body=Please+file+an+issue+if+the+maintained+button+says+no)
[![PyPI Status](https://img.shields.io/pypi/status/quickdiary.svg?style=flat-square&label=pypi-status)](https://pypi.python.org/pypi/quickdiary)
[![PyPI Version](https://img.shields.io/pypi/v/quickdiary.svg?style=flat-square)](https://pypi.python.org/pypi/quickdiary)
[![PyPI Python Versions](https://img.shields.io/pypi/pyversions/quickdiary.svg?style=flat-square)](https://pypi.python.org/pypi/quickdiary)

## Requirements

```
                                                               ┌──────────────┐
                                                               │ GNU/Linux    │
                                                               │ Python 3     │
                                                               │ Python 3 Pip │
                                                               └──────────────┘
```

## Installing

```
pip install quickdiary
```

## Usage

```sh
quickdiary
```

The name is long because is expected the user to create his own alias, for example, add to `.bashcr` or `.zshrc` or similar the alias below.

**If no filename is given** in the command-line/command alias, it defaults to `~/diary.quickdiary`. Why such an absurd name and place, you may ask? That's because we think it is better the user itself in their alias to choose his own filenames for diaries as needed; we, though, suggest you use one of the file extensions `.quickdiary` or `.qdiary` so that it is easier to find the files later on the filesystem, being that you can have various different diaries with different names in different places.

#### Adding alias

```
alias qd='quickdiary prompt'
```

Then you use the command `qd` to quickly add a timestamped text entry.

## Options

```sh
$ quickdiary --help
Usage: quickdiary [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  cat     Prints the diary file to stdout.
  edit    Opens the diary file in $EDITOR or $QUICKDIARY_EDITOR.
  pager   Opens the diary file in $PAGER or $QUICKDIARY_PAGER.
  prompt  Prompts for the entry to be added to the diary.
  write   Writes to diary using configured editor.
```

You also can see each command's help using `quickdiary <command> --help`, *eg*.:

### quickdiary write

```sh
$ quickdiary write --help
Usage: quickdiary write [OPTIONS]

  Writes to diary using configured editor.

Options:
  -f, --file <filename>  File to add entry
  --help                 Show this message and exit.

  Writes to diary file using $EDITOR or $QUICKDIARY_EDITOR
```

### quickdiary prompt

```sh
$ quickdiary prompt --help
Usage: quickdiary prompt [OPTIONS]

  Prompts for the entry to be added to the diary.

Options:
  -f, --file <filename>  File to add entry
  -t, --text <text>      Text entry to write to the diary
  --help                 Show this message and exit.

  Prompts for the text to add to the diary.
```

### quickdiary edit

```sh
$ quickdiary edit --help
Usage: quickdiary edit [OPTIONS]

  Opens the diary file in $EDITOR or $QUICKDIARY_EDITOR.

Options:
  -f, --file <filename>  File to add entry
  --help                 Show this message and exit.

  Opens the diary file in the configured text editor.
```

### quickdiary pager

```sh
$ quickdiary pager --help
Usage: quickdiary pager [OPTIONS]

  Opens the diary file in $PAGER or $QUICKDIARY_PAGER.

Options:
  -f, --file <filename>  File to add entry
  --help                 Show this message and exit.

  Opens the diary file in the configured environment pager.
```

### quickdiary cat

```sh
$ quickdiary cat --help
Usage: quickdiary cat [OPTIONS]

  Prints the diary file to stdout.

Options:
  -f, --file <filename>  File to add entry
  --help                 Show this message and exit.

  Prints the diary file to stdout.
```


## Environment Variables

These variables can be set in you env to change quicidiary defaults.

```sh
export QUICKDIARY_FILENAME="~/diary.quickdiary"
export QUICKDIARY_DATE_FORMAT="%A, %B {day_of_month}, %Y"
export QUICKDIARY_TIME_FORMAT "%H:%M:%S: "
export QUICKDIARY_EDITOR="$EDITOR"
export QUICKDIARY_EDITOR_PARAMS="+norm GA"  # in vim, go to the end of the last line
export QUICKDIARY_PAGER="$PAGER"
export QUICKDIARY_PAGER_PARAMS=""
export QUICKDIARY_PRE_DATE_STRING="\n\n"  # only if it's not a new file
export QUICKDIARY_PRE_ENTRY_STRING="\n\n"
```

The variables for date and time are [those from python's `strftime`](https://docs.python.org/3/library/datetime.html?highlight=strftime#strftime-and-strptime-format-codes)

Description of the ENV variables:

**QUICKDIARY_FILENAME** - Is the diary filename; it will be created if it doesn't exist.

**QUICKDIARY_DATE_FORMAT** - Is the date format. It is added one time a day, when the first entry of the day is added.

**QUICKDIARY_TIME_FORMAT** - It is the time format for each entry. It is added before each entry.

**QUICKDIARY_EDITOR** - When in `edit` mode, this will be the editor with which edit the new entry. (Default for env's $EDITOR, expecting it is `vim`/`nvim`)

**QUICKDIARY_EDITOR_PARAMS** - These are the parameters to be passed to the editor before the diary file name. Defaults to *vim*'s "**+norm GA**" which in *normal mode* (**+norm**) *goes to the end of the file* (**G**) and to the end of that line (**A**). As said before, it is expected the user uses vim, otherwise these parameters need to be changed or nulled, like this way:

**QUICKDIARY_PAGER** - It is the pager used in `pager` mode.

**QUICKDIARY_PAGER_PARAMS** - These are the pager parameters for the pager in `pager` mode.

**QUICKDIARY_PRE_DATE_STRING** - String to add before dates to saparate from the past items etc. Newlines. It is not added when on a new file, as in this case there are no previous items.

**QUICKDIARY_PRE_ENTRY_STRING** - String to add before diary entries to separate them from the past items; how many newlines to separate them etc.

```sh
export QUICKDIARY_EDITOR_PARAMS=""
```

## Develpoment & Philosophy

The idea is having a simple program to manage quick diary entries or notes, time stamped.

Notes should be able to comply to all of these:

* Quick to add, *eg*.: terminal command-alias `qd` -> type text line -> press enter, done; inserted in date and with current time.
* Possibility to rich-edit using editor, *eg*: type alias `qde` -> open text editor with the cursor in place -> edit -> save, done. This withouth corrupting the following:
* Easily readable programatically, so we can program features over the notes.
* Easily human-readable.
* After and only after all these, should be customizable.

So new features will be developed based on these points.
