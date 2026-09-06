import base64
import os

from pathlib import Path
from typing import Generator, Any


def yield_file_abs_path(folder_path: str) -> Generator[str | Any, Any, None]:
    with os.scandir(folder_path) as entries:
        for entry in entries:
            if entry.is_file():
                yield entry.path
            elif entry.is_dir():
                yield_file_abs_path(entry.path)


def get_file_name(file_path: str) -> str:
    return Path(file_path).name


def get_file_stem(file_path: str) -> str:
    return Path(file_path).stem


def read_file_text(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def read_file_bytes(file_path: str) -> bytes:
    with open(file_path, 'rb') as file:
        return file.read()


def write_text_to_file(file_path: str, data: str) -> None:
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(data)


def encode_2_base64(data_bytes: bytes) -> bytes: # TODO
    return base64.b64encode(data_bytes)