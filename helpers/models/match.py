#! /usr/bin/env python3

class MatchedElement:
    def __init__(self, file_path: str, file_line: int, is_regex: bool, line_value: str, signature_name: str,
                 pattern: str, is_binary: bool):
        self.file_path = file_path
        self.file_line = file_line
        self.is_regex = is_regex
        self.line_value = line_value
        self.signature_name = signature_name
        self.pattern = pattern
        self.is_binary = is_binary
