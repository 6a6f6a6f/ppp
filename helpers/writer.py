#! /usr/bin/env python3

from sys import stderr

from termcolor import colored, cprint


def bold(text: str, color: str = '') -> str:
    return colored(text, attrs=['bold']) if not color else colored(text, attrs=['bold'], color=color)


def panic(text: str):
    cprint(bold('Panic: ', 'red') + text, file=stderr)
    exit(-1)


def error(text: str):
    print(f'{bold("e", "red")} {text}')


def info(text: str):
    print(f'{bold("i", "blue")} {text}')


def item(text: str):
    print(f'  {bold("↦", "green")} {text}')


def warn(text: str):
    print(f'{bold("w", "yellow")} {text}')


def success(text: str):
    print(f'{bold("s", "green")} {text}')
