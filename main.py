#! /usr/bin/env python3
import os
from shutil import rmtree
from sys import argv

from colorama import init

from helpers.handlers.adb import get_device, get_app
from helpers.io import dump_app
from helpers.writer import info, bold, panic


def main():
    init()

    info(f'{bold("PPP")} - {bold("P")}roxy {bold("p")}ara {bold("P")}reguiçosos.')
    info(f'Writen by {bold("Jojo <jonas.uliana at passwd.com.br>")}.')
    info(f'For help, get in touch via {bold("keybase.io/bizarrenull")}.\n')

    if len(argv) < 2:
        info(bold('Usage examples: '))
        info(f'List available signatures   {bold("list signatures")}')
        info(f'Try to list signatures for  {bold("detect com.application")}')
        info(f'Setup and run Frida against {bold("com.application")}\n')
        panic('You need at least one argument!')

    device = get_device()
    info(f'Using device {bold(device)} as the pwning host.')
    app_name, app_path = get_app(argv[1], device)
    info(f'Analysing app {bold(app_name)}...')
    path = dump_app(app_path, device)
    info('Package dumped...')
    info(f'Analysing {len(os.listdir(path))} file(s)...')
    rmtree(path, ignore_errors=True)


if __name__ == '__main__':
    main()
