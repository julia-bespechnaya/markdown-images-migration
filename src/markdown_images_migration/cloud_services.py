from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import List

import requests

from markdown_images_migration.constants import IMGBB_API_URL
from markdown_images_migration.images import EncodeType, ImageFile


class CloudName(Enum):
    ImgBB = 'ImgBB'

    @classmethod
    def get(cls, pattern_value: str) -> 'CloudName':

        match pattern_value:
            case cls.ImgBB.value:
                return cls.ImgBB
            case _:
                raise ValueError('Cloud Name is incorrect')

    @classmethod
    def get_api_url(cls, cloud_name: 'CloudName') -> str:

        match cloud_name:
            case cls.ImgBB:
                return IMGBB_API_URL
            case _:
                raise ValueError('This Cloud Name does not exist')


@dataclass
class CloudService(ABC):
    name: CloudName
    api_url: str
    data_encode_type: EncodeType

    @abstractmethod
    def post_image(self, image, api_key: str) -> tuple[str, int]:
        pass


    def post_images(self, images: List[ImageFile], api_key: str) -> list[str]:
        images_urls = []

        for image_file in images:
            image_url, response_status_code = self.post_image(image_file, api_key)

            if response_status_code != StatusCode.SUCCESS.value:
                raise ValueError('Image was not uploaded!')

            images_urls.append(image_url)

        return images_urls


@dataclass
class ImgbbCloud(CloudService):
    name: CloudName = CloudName.ImgBB
    api_url: str = CloudName.get_api_url(name)
    data_encode_type: EncodeType = EncodeType.BASE64

    def post_image(self, image_file: ImageFile, api_key: str) -> tuple[str, int]:

        params = {'key': api_key,
                  'name': image_file.stem}

        data = {'image': image_file.encoded_data}

        response = requests.post(self.api_url, params=params, data=data)

        return response.json()['data']['url'], response.status_code


def init_cloud_service(cloud_name: CloudName) -> CloudService:

    match cloud_name:
        case CloudName.ImgBB:
            return ImgbbCloud()
        case _:
            raise ValueError('Cloud Service Name is incorrect')


class CloudServiceFactory:
    _clouds = {
        'imgbb': ImgbbCloud
    }

    @classmethod
    def create(cls, cloud_name: str) -> CloudService:
        try:
            cloud_class = cls._clouds[cloud_name.lower()]
        except KeyError:
            raise ValueError(f'Unknown cloud service: {cloud_name}')
        return cloud_class()


class StatusCode(Enum):
    SUCCESS = 200


