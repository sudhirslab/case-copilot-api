import requests
from PIL import Image
from io import BytesIO
import os


"""
Generate a thumbnail for an image

Args:
    file_url (str): The URL of the image.
    output_path (str): The path to save the thumbnail.
    width (int): The width of the thumbnail.
"""
def generate_thumbnail(file_url: str, output_path: str, width: int = 200) -> str:
    print('Current working directory:', os.getcwd())
    try:
        response = requests.get(file_url)
        response.raise_for_status()

        print(f"Generating thumbnail for {file_url}")

        image = Image.open(BytesIO(response.content))

        aspect_ratio = image.height / image.width
        new_height = int(width * aspect_ratio)
        thumbnail = image.resize((width, new_height))

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        thumbnail.save(output_path)
        print(f"Thumbnail saved to {output_path}")
        return output_path

    except Exception as e:
        print('Error generating thumbnail:', str(e))
        raise
