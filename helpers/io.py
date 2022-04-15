#! /usr/bin/env python3
import sys
import tempfile
import uuid
from os import path
from shutil import rmtree

from helpers.handlers.adb import run_command
from helpers.writer import panic


def dump_app(package_path: str, device: str) -> str:
    temp_dir = path.join("/tmp" if sys.platform == "darwin" else tempfile.gettempdir(), str(uuid.uuid4().hex))

    _, stdout, _ = run_command(f'shell ls {package_path}', device)
    packages = list(
        (file for file in stdout.split('\n') if file.endswith('.apk'))
    )

    if len(packages) == 0:
        panic('Unable to find any .apk inside the package installation directory!')

    for package in packages:
        run_command(f'pull {package_path}/{package} {path.join(temp_dir, package)}', device)

    code, _, _ = run_command(f'pull {package_path} {temp_dir}', device)
    if code == 1:
        panic('Unable to dump the application!')
        rmtree(temp_dir, ignore_errors=True)

    return temp_dir
