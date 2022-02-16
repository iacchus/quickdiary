# quickdiary 

| **Licensed with [GNU AGPLv3](https://github.com/iacchus/agplv3-resources/blob/master/LICENSE/LICENSE)**                                                                        |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [![agpl3](https://raw.githubusercontent.com/iacchus/agplv3-resources/main/LICENSE/agplv3-155x51.png)](https://github.com/iacchus/agplv3-resources/blob/master/LICENSE/LICENSE) |

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

```
quickdiary
```

The name is long because is expected the user to create his own alias, for example, add to `.bashcr` or `.zshrc` or similar:

#### Adding alias

```
alias qd='quickdiary'
```

## Environment Variables

These variables can be set in you env to change quicidiary defaults.

```sh
export QUICKDIARY_FILENAME="~/diary.quickdiary"
export QUICKDIARY_DATE_FORMAT="%A, %B {day_of_month}, %Y"
export QUICKDIARY_TIME_FORMAT "%H:%M:%S: "
export QUICKDIARY_EDITOR="$EDITOR"
export QUICKDIARY_EDITOR_PARAMS="+norm GA"  # in vim, go to the end of the last line
```

The variables for date and time are [those from python's `strftime`](https://docs.python.org/3/library/datetime.html?highlight=strftime#strftime-and-strptime-format-codes)

Description of the ENV variables:

**QUICKDIARY_FILENAME** - Is the diary filename; it willbe created if it doesn't exist.

**QUICKDIARY_DATE_FORMAT** - Is the date format. It is added one time a day, when the first entry of the day is added.

**QUICKDIARY_TIME_FORMAT** - It is the time format for each entry. It is added before each entry.

**QUICKDIARY_EDITOR** - When in editor mode (without `--prompt`), this will be the editor with which edit the new entry. (Default for env's $EDITOR, expecting it is `vim`/`nvim`)

**QUICKDIARY_EDITOR_PARAMS** - These are the parameter to be passed to the editor before the diary file name. Defaults to vim '+norm GA' which in *normal mode* (**+norm**) *goes to the end of the file* (**G**) and to the end of that line (**A**). As said before, it is expected the user uses vim, otherwise these parameters need to be changed or nulled, like this way:


```
export QUICKDIARY_EDITOR_PARAMS=""
```
