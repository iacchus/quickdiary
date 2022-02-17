# quickdiary 

| **Licensed with [GNU AGPLv3](https://github.com/iacchus/agplv3-resources/blob/master/LICENSE/LICENSE)**                                                                        |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [![agpl3](https://raw.githubusercontent.com/iacchus/agplv3-resources/main/LICENSE/agplv3-155x51.png)](https://github.com/iacchus/quickdiary/blob/main/LICENSE.txt) |

Simple command to add timestamped entries to a text file using `$EDITOR`.

## Requirements

* GNU/Linux
* Python 3
* Python 3 Pip

## Installing

```
pip install quickdiary
```

## Usage

```sh
quickdiary
```

The name is long because is expected the user to create his own alias, for example, add to `.bashcr` or `.zshrc` or similar:

#### Adding alias

```
alias qd='quickdiary'
```

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

```sh
export QUICKDIARY_EDITOR_PARAMS=""
```
