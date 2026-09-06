from markdown_images_migration.cloud_services import CloudServiceFactory, CloudName
from markdown_images_migration.md_files import build_image_files_from_md_file, MarkdownFile, ImageLink
from markdown_images_migration.regex import PatternRule

from markdown_images_migration.constants import MD_FILE_PATH, IMAGES_FOLDER_PATH, IMGBB_API_KEY


def migrate_md_file_images(md_file_path: str, cloud_name: str, images_folder_path: str, image_name_pattern: str, api_key: str) -> None:
    """Migrates images that are used in a Markdown file to the specified cloud service, changes image urls in a Markdown file to new urls

        Parameters
        ----------
        md_file_path : str
            Absolute path to the Markdown file on your device for which you want to migrate all images to the specified cloud service.
        cloud_name : str
            Name of the cloud service to which you want to migrate images.
            In the current version of the package you can choose from these options:
                - 'imgbb' - free cloud service for storing images. Official site: https://imgbb.com
        images_folder_path : str
            Absolute path to the directory where all images for the Markdown file are stored on your device.
        image_name_pattern : str
            Pattern rule for names of images which belong to the Markdown file.
            This pattern rule will be used to detect images which belong to the Markdown file by the Markdown file name (for example: 'md_file_name').
            In the current version of the package you can choose from these options:
                - 'string prefix' - images name start with a name of the Markdown file
                    Pattern: {md file name}_{any text}
                    Examples of image names: md_file_name_1, md_file_name_24, md_file_name_anytext
                - 'file prefix' - images name start with a name of the Markdown file + its resolution
                    Pattern: {md file name}.md_{any text}
                    Examples of image names: md_file_name.md_1, md_file_name.md_24, md_file_name.md_anytext
                - 'image file prefix' - images name start with a word image + name of the Markdown file + its resolution
                    Pattern: image_[{md file name}.md]_{any text}
                    Examples of image names: image_[md_file_name.md]_1, image_[md_file_name.md]_24, image_[md_file_name.md]_anytext
        api_key : str
            API key for your account from the specified cloud service that can be used to upload images on this cloud service

        Returns
        -------
        None
        """

    cloud_service = CloudServiceFactory.create(cloud_name)

    image_files = build_image_files_from_md_file(md_file_path, images_folder_path, image_name_pattern)

    md_file = MarkdownFile(md_file_path)

    image_links: list[ImageLink] = [ImageLink(md_file, image_file) for image_file in image_files]

    current_images_urls = md_file.extract_image_urls()

    if len(current_images_urls) != len(image_files):
        raise ValueError('Image urls in markdown file and Image files in images folder do not match!')

    for image_file in image_files:
        image_file.encode_image(cloud_service.data_encode_type)

    new_images_urls = cloud_service.post_images(image_files, api_key)

    for image_link, current_image_url, new_image_url in zip(image_links, current_images_urls, new_images_urls):
        if not image_link.old_urls:
            image_link.old_urls = [current_image_url]
        else:
            image_link.old_urls.append(current_image_url)
        image_link.current_url = new_image_url

    md_file.update_image_urls(image_links)

    print('Migration is successful!')


if __name__ == '__main__':
    migrate_md_file_images(MD_FILE_PATH, CloudName.ImgBB.value, IMAGES_FOLDER_PATH, PatternRule.IMAGE_FILE_PREFIX.value, IMGBB_API_KEY)