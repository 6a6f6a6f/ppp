#! /usr/bin/env python3

from shutil import which
from subprocess import run, Popen

from helpers.writer import panic


def get_adb() -> str:
    adb_path = which('adb')
    if adb_path is None:
        panic('Unable to find ADB in your $PATH!')
    return adb_path


def get_device() -> str:
    command_device = run(f'"{get_adb()}" devices', capture_output=True, shell=True, universal_newlines=True)
    if command_device.returncode != 0:
        panic('Unable list available devices, check your ADB daemon!')

    lines = command_device.stdout.strip().split('\n')
    devices = []
    del lines[0]
    for line in lines:
        if 'device' not in line:
            continue
        device = line.split()
        devices.append(device[0])

    if len(devices) == 0:
        panic('There is no available device!')
    if len(devices) > 1:
        panic('There is more than one available device!')

    return devices[0]


def run_command_background(command: str, device: str) -> (int, str, str):
    cmd = Popen([get_adb(), '-s', device] + command.split())
    return cmd.returncode, cmd.stdout, cmd.stderr


def run_command(command: str, device: str) -> (int, str, str):
    cmd = run(f'"{get_adb()}" -s {device} {command}', capture_output=True, shell=True, universal_newlines=True)
    return cmd.returncode, cmd.stdout.strip(), cmd.stderr.strip()


def get_app(package: str, device: str) -> (str, str, str):
    code, stdout, _ = run_command(f'shell pm list packages -f -3 {package}', device)
    if code == 1:
        panic('Unable to find any Android application by given name!')

    packages = stdout.split('\n')
    if len(packages) > 1 or not packages[0]:
        panic(f'Unable to find a unique packages by current criteria!')

    tmp = packages[0].split(':')[1]
    k = tmp.rfind('/')
    path = ''
    for i in range(k):
        if not i > k:
            path += tmp[i]
    return packages[0].split('/')[-1].split('=')[1], path
