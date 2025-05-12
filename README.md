# TemplateCreator

A tool that can pack a folder with subfiles into an archive, which can be customized once extracted !
The script is OS agnostic, which means that the files will be created regardless of the OS, since they're
expressed internally as relative paths (strings).

## How does it works ?

Create a folder structure, with files that you're going to use as template.
When you want a word / phrase to be customized, add the tokens (by default ##) before and after it.

```
I'm getting ##customized##
```

Here, the word customized will be changed when extracted !
This also work if you have multiple variables in the same line.

The base file, which can contain the project name can be fully customized, including it's name !

All text files are supported (Tex, Py, Makefile...). Binary files are simply ignored, but replicated.

### Creating an archive :

Launch the tool, you will be asked to input a reference path to create. You then need to choose which file is
the "main", which will then be renamed.

Let the tool compute everything as needed, you'll end up with a data.template file on the root of the folder structure.

This archive can be renamed without any issues, it's even recommended ! You can have multiple archive in the same folder.

### Openning an archive

Place the archive in the folder where it will be expanded, and then, call the Python tool.
The tool will proceed to some safety check to ensure the file wasn't modified since creation, and then, will create files and
folder if needed.

You can then use any tool you want !

## Technicals details

Under the hood, some aspects are required to ensure the file will be correctly generated.
This include :

- Reading text files only
- Compressing data
- Computing an SHA3_512 hash of the data
- Write to file (using pickle module)

- ...

- Reading the template file
- Ensuring hash match
- Decompressing data
- Customizing files
- Outputing files.

## How to use it ?

There is multiple ways to use it !
The first is from the command line.

### Writter :

Invoke tcreator-write-[aarch ]-[OS ] command, with the following settings :

```
usage: tcreator-write [-h] [-o OUTPUT] [-v] [-t TOKEN] [-p PROJECT] folder file

Create a template from a used folder

positional arguments:
  folder                Pass the folder you want to zip into a template
  file                  Pass the file for which the name can be customized (ex : main file)

options:
  -h, --help            show this help message and exit
  -o, --output OUTPUT   Change the output location of the template file.
  -v, --verbose         Add logs output for the user
  -t, --token TOKEN     Change the parsed token to identify variables. Can be usefull is your langage use the default one '##'
  -p, --project PROJECT
                        Change the name of the variable that is used as name for file, or any other customization.
```

### Openner :

```
usage: tcreator-open [-h] [-i] [-o OUTPUT] [-v] template

Open a .template file and expand it.

positional arguments:
  template             Pass the .template file to be openned.

options:
  -h, --help           show this help message and exit
  -i, --ignorev        Indicate to the script to ignore the input for the variables. Recommended for automated usages, not for final user.
  -o, --output OUTPUT  Change the output destination of the expanded folder
  -v, --verbose        Add logs output when running the command

WARNING : Actually, this tool will ask the user inputs. In case of automated use, set --ignorev to True to block this behavior. Variables will be left untouched then.
```

### GUI

> [!WARNING]
> The GUI does not support full featured operations, such as token customization or main variable name change. For theses operations, the usage
> the command line is recommended.

The GUI does not require any arguments.
Just launch :

```
tcreator
```

and the GUI will pop-up by itself. You then will be guided by choices and pop up !
