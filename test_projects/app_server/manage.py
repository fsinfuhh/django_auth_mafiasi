#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path


def main():
    """Run administrative tasks."""
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    sys.path.append(str(BASE_DIR / "src"))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app_server.settings")
    os.environ.setdefault("DJANGO_CONFIGURATION", "Dev")
    from configurations.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
