#! /usr/bin/env python3
import os
from shutil import rmtree
from sys import argv

from colorama import init

from helpers.handlers.adb import get_device, get_app
from helpers.io import dump_app, decode_app
from helpers.writer import info, bold, panic, success, item


def main():
    init()

    info(f'{bold("PPP")} - {bold("P")}roxy {bold("p")}ara {bold("P")}reguiçosos.')
    info(f'Writen by {bold("Jojo <jonas.uliana at passwd.com.br>")}.')
    info(f'For help, get in touch via {bold("keybase.io/bizarrenull")}.')
    info('PS: I \'m not a Python developer.\n')

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
    dump_path = dump_app(app_path, device)
    info('Package dumped...')

    for apk in os.listdir(dump_path):
        apk_path = os.path.join(dump_path, apk)
        if not os.path.isfile(apk_path):
            continue
        matched_signatures = decode_app(apk, dump_path)
        if len(matched_signatures) > 0:
            print()
            for element in matched_signatures:
                if not element.is_binary:
                    success(f'{bold(element.signature_name)} (.smali):')
                    item(f'Detected on {bold(element.file_path)}:{bold(str(element.file_line))}')
                    item(f'With pattern "{bold(element.pattern)}"')
                    item(f'Raw value is "{bold(element.line_value.strip())}"')
                    print()
                else:
                    print(element.signature_name)

    rmtree(dump_path, ignore_errors=True)


if __name__ == '__main__':
    main()
