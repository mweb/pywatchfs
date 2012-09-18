pywatchfs
=========

A simple script to track all files accessed within a directory.

Usage
-----

  usage: pywatchfs.py [-h] [--verbose] [--version] [--output OUTPUT] path

  Listen on a directory for all kind of file access.

  positional arguments:
    path                  The directory to observer

  optional arguments:
    -h, --help            show this help message and exit
    --verbose, -v         enable verbose output
    --version             show program's version number and exit
    --output OUTPUT, -o OUTPUT
                          Use the given file as output instead of the stdout

TODO
----

- The output parameter is currently not working
- A filtered output instead of the live output would be nice
