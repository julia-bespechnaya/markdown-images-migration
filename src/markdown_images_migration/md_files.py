import re

from dataclasses import dataclass, field

from markdown_images_migration.files import get_file_name, yield_file_abs_path, get_file_stem, \
    read_file_text, write_text_to_file
from markdown_images_migration.images import ImageFile, is_valid_image_file
from markdown_images_migration.regex import PatternRule, is_str_match_pattern


def is_image_from_md_file(md_file_path: str, image_path: str, image_name_pattern: str) -> bool:
    md_file_name = get_file_name(md_file_path)
    image_name_pattern = PatternRule.get(image_name_pattern) # TODO: try except?
    str_used_in_pattern = PatternRule.get_string_4_pattern(image_name_pattern, md_file_name)

    image_name = get_file_name(image_path)
    return is_str_match_pattern(image_name, image_name_pattern, str_used_in_pattern)


def build_image_files_from_md_file(md_file_path: str,
                                   images_folder_path: str,
                                   image_name_pattern: str) -> list[ImageFile]:
    image_files_from_md_file = []

    for file_path in yield_file_abs_path(images_folder_path):
        if not is_valid_image_file(file_path) or not is_image_from_md_file(md_file_path, file_path, image_name_pattern):
            continue

        image_files_from_md_file.append(ImageFile(file_path))

    return image_files_from_md_file


def get_images_urls_from_md_file(md_file_content: str) -> list[str]:
    # Markdown image
    # ![Title of image](URL to image)
    return re.findall(r'!\[.*]\((.*)\)', md_file_content)


@dataclass
class MarkdownFile:
    path: str
    name: str = field(init=False)
    _content: str = field(init=False)

    def __post_init__(self):
        self.stem = get_file_stem(self.path)
        self._content = read_file_text(self.path)


    @property
    def content(self) -> str:
        return self._content

    @content.setter
    def content(self, content: str) -> None:
        write_text_to_file(self.path, content)
        self._content = content


    def extract_image_urls(self) -> list[str]:
        return get_images_urls_from_md_file(self._content)


    def update_image_urls(self, image_links: list['ImageLink']):
        updated_content = self.content

        for image_link in image_links:
            updated_content = updated_content.replace(image_link.old_urls[-1], image_link.current_url)

        self.content = updated_content
        # TODO if did not written return something


@dataclass
class ImageLink:
    md_file: MarkdownFile
    image_file: ImageFile
    current_url: str = None
    old_urls: list[str] = None