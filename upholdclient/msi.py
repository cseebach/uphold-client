__author__ = 'cseebach'

import subprocess
import os.path


def validate(task):
    return (
        "msi" in task and
        isinstance(task["msi"], basestring) and
        task["msi"].endswith(".msi") and
        os.path.exists(task["msi"]))


def call(msi_task):
    return not subprocess.call(["msiexec", "/i", msi_task["msi"], "/qn"])


def pretty_print(msi_entry):
    return msi_entry



