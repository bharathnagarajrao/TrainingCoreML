import requests
import shutil
import os

def download_images(url_filename, out_directory, max_urls=None):
    """Download images from a file containing URLS.

    The URL file must contain a single URL per line.

    Args:
        url_filename (str): a file containing urls
        out_directory (str): a path to save downloaded images
        num_urls (int optional): a maximum number of urls to try.
            Useful for prototyping.

    Returns:
        errors List[str]: a list of urls that could not be downloaded
    """
    img_idx = 0
    url_idx = 0
    errors = []
    with open(url_filename) as urls:
        for url in urls.readlines():
            url = url.rstrip()  # Remove the newline
            try:
                # Request the url and check the status of the response.
                response = requests.get(url, timeout=2.0, stream=True)
                if response.status_code != 200:
                    raise Exception('Not 200')

                # Save the bytes to a file.
                image_filename = os.path.join(
                    out_directory, '%05d.jpg' % img_idx
                )
                with open(image_filename, 'w') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                img_idx += 1

            except Exception as err:
                errors.append(url)
            url_idx += 1
            if max_urls and url_idx >= max_urls:
                break
    print 'Tried %d urls and successfully downloaded %d images.' % (url_idx, img_idx)
    return errors


if __name__ == "__main__":
    download_images("<Enter your source path>", "<Enter your destination path>")
