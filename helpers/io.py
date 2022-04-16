#! /usr/bin/env python3
import glob
import os.path
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import uuid
from os import path

from helpers.handlers.adb import run_command
from helpers.models import signature
from helpers.models.match import MatchedElement
from helpers.writer import panic, info, bold


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
        shutil.rmtree(temp_dir, ignore_errors=True)
        panic('Unable to dump the application!')

    return temp_dir


def _smali_detect(file_path: str) -> list[MatchedElement]:
    signatures = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
        counter = 0
        for line in lines:
            counter += 1
            for sig in signature.smali:
                for rule in signature.smali[sig]:
                    match = rule['literal']
                    is_regex = bool(rule['regex'])
                    better_file = pathlib.Path(file_path).name
                    match_model = MatchedElement(better_file, counter, is_regex, line, sig, match, False)
                    if is_regex:
                        valid = re.findall(line, match)
                        if len(valid) > 0:
                            signatures.append(match_model)
                    if not is_regex and match in line:
                        signatures.append(match_model)
    return signatures


# def native_detect(file_path: str):
# ignored


def decode_app(apk_file: str, working_folder: str) -> list[MatchedElement]:
    apktool_path = _get_apktool()
    if not apktool_path:
        shutil.rmtree(working_folder, ignore_errors=True)
        panic('apktool does not exist in $PATH!')
    origin = os.path.join(working_folder, apk_file)
    destination = os.path.join(working_folder, pathlib.Path(apk_file).stem)
    cmd = subprocess.run(f'{apktool_path} d {origin} -o {destination}',
                         capture_output=True, shell=True, universal_newlines=True)
    if cmd.returncode != 0:
        shutil.rmtree(working_folder, ignore_errors=True)
        panic(f'apktool was unable to decode {apk_file}!')
    files = _get_full_path_files(destination)
    info(f'Analysing {bold(apk_file)} with {len(files)} artifact(s)...')

    signatures = []
    for file in files:
        if not os.path.isfile(file):
            continue

        if pathlib.Path(file).suffix == '.smali':
            smali_signatures = _smali_detect(file)
            if len(smali_signatures) > 0:
                signatures.extend(smali_signatures)

        # if pathlib.Path(file).suffix == '.so':
        #     native_detect(file)
    return signatures


def _get_full_path_files(origin_path: str) -> list[str]:
    col = []
    for filename in glob.iglob(f'{origin_path}/**/*', recursive=True):
        col.append(os.path.abspath(filename))
    return col


def _get_apktool() -> str:
    tool_path = shutil.which('apktool')
    return tool_path if tool_path else ''
