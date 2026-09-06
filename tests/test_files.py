import pytest

from markdown_images_migration.files import get_file_name, get_file_stem, read_file_text, read_file_bytes
from tests.constants import IMAGE_PATH, MD_FILE_PATH


@pytest.mark.parametrize(
    'file_path, expected',
    [
        (IMAGE_PATH, 'test_image.jpg')
    ]
)
def test_get_file_name(file_path, expected):
    result = get_file_name(file_path)
    assert result == expected


@pytest.mark.parametrize(
    'file_path, expected',
    [
        (IMAGE_PATH, 'test_image')
    ]
)
def test_get_file_stem(file_path, expected):
    result = get_file_stem(file_path)
    assert result == expected


@pytest.mark.parametrize(
    'file_path, expected',
    [
        (MD_FILE_PATH, '# Title\n\nContent of a page\n\n![test_image]()')
    ]
)
def test_read_file_text(file_path, expected):
    result = read_file_text(file_path)
    assert result == expected


@pytest.mark.parametrize(
    'file_path, expected',
    [
        (MD_FILE_PATH, b'# Title\r\n\r\nContent of a page\r\n\r\n![test_image]()')
    ]
)
def test_read_file_bytes(file_path, expected):
    result = read_file_bytes(file_path)
    assert result == expected

