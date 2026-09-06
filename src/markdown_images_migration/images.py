from dataclasses import dataclass, field
from enum import Enum
from typing import Callable

from PIL import Image

from markdown_images_migration.files import encode_2_base64, read_file_bytes, get_file_stem


class EncodeType(Enum): #TODO
    BASE64 = 'base64'

    @classmethod
    def get_encode_method(cls, encode_type: 'EncodeType') -> Callable[[bytes], bytes]:

        match encode_type:
            case cls.BASE64:
                return encode_2_base64
            case _:
                raise ValueError('This Encode Type does not exist')


@dataclass
class ImageFile:
    path: str
    stem: str = field(init=False)

    data: bytes = field(init=False)
    encode_type: EncodeType = None
    encoded_data: bytes = None

    def __post_init__(self) -> None:
        self.stem = get_file_stem(self.path)
        self.data = read_file_bytes(self.path)

    def encode_image(self, encode_type: EncodeType) -> None:
        encode_method = EncodeType.get_encode_method(encode_type)

        self.encoded_data = encode_method(self.data)
        self.encode_type = encode_type


def is_valid_image_file(file_path: str) -> bool:
    try:
        with Image.open(file_path) as img:
            img.verify()
            return True
    except(IOError, SyntaxError):
        return False