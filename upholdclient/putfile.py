__author__ = 'cseebach'

import shutil
import os.path


def validate(putfile_entry):
    return (
        "file" in putfile_entry and
        "into" in putfile_entry and
        os.path.exists(putfile_entry["file"]))


def call(putfile_entry):
    try:
        shutil.copy(putfile_entry["file"], putfile_entry["into"])
        return True
    except (OSError, IOError):
        return False


def pretty_print(putfile_entry):
    return "file: {}, into: {}".format(putfile_entry["file"], putfile_entry["into"])
