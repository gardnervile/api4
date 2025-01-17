import argparse
import requests
import os
from utils import create_folder, download_image, get_file_extension

def fetch_spacex_images(launch_id=None, folder_name="spacex_images"):
    create_folder(folder_name)
    url = f"https://api.spacexdata.com/v5/launches/{launch_id or 'latest'}"
    
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    photos = data.get("links", {}).get("flickr", {}).get("original", [])
    
    if not photos:
        raise ValueError("Фотографий для запуска не найдено.")
    
    for i, photo_url in enumerate(photos, start=1):
        file_name = f"spacex_photo_{i}{get_file_extension(photo_url)}"
        download_image(photo_url, os.path.join(folder_name, file_name))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Скачивание фотографий SpaceX.")
    parser.add_argument("--id", help="ID запуска SpaceX. Если не указан, скачиваются фото с последнего запуска.")
    args = parser.parse_args()
    
    try:
        fetch_spacex_images(launch_id=args.id)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
    except ValueError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
