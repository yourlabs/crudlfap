#!/usr/bin/env python
import os
import sys


def main():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "crudlfap_example.settings"
    )
    from django.core.management import execute_from_command_line
    if sys.argv[1] == 'shell' and len(sys.argv) == 2:
        import readline
        import atexit
        histfile = os.path.join(os.path.expanduser("~"), ".django_history")

        try:
            readline.read_history_file(histfile)
            h_len = readline.get_current_history_length()
        except FileNotFoundError:
            open(histfile, 'wb').close()
            h_len = 0

        def save(prev_h_len, fname):
            new_h_len = readline.get_current_history_length()
            readline.set_history_length(1000)
            readline.append_history_file(new_h_len - prev_h_len, fname)

        atexit.register(save, h_len, histfile)

    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
