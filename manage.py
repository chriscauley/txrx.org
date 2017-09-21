#!/usr/bin/env python
import warnings
warnings.filterwarnings("ignore")

import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

