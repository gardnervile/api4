import os
import requests
from urllib.parse import urlsplit, unquote

def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def get_file_extension(url):
    path = urlsplit(url).path
    decoded_path = unquote(path)
    _, file_extension = os.path.splitext(os.path.split(decoded_path)[1])
    return file_extension

def download_image(image_url, save_path):
    response = requests.get(image_url, stream=True)
    response.raise_for_status()
    with open(save_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    print(f"Изображение сохранено: {save_path}")


if __name__ == "__main__":
    image_url = "https://example.com/image.png"
    save_path = "images/image.png"
    
    create_folder(os.path.dirname(save_path))
    
    try:
        download_image(image_url, save_path)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при скачивании {image_url}: {e}")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
