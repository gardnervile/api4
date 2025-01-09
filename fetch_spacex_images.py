import argparse
import requests
import os
from main import create_folder, download_image, get_file_extension

def fetch_spacex_images(launch_id=None, folder_name="spacex_images"):
    create_folder(folder_name)
    url = "https://api.spacexdata.com/v5/launches"
    url += f"/{launch_id}" if launch_id else "/latest"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        photos = data.get("links", {}).get("flickr", {}).get("original", [])
        if not photos:
            print("Фотографий для запуска не найдено.")
            return
        for i, photo_url in enumerate(photos, start=1):
            file_name = f"spacex_photo_{i}{get_file_extension(photo_url)}"
            download_image(photo_url, os.path.join(folder_name, file_name))
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Скачивание фотографий SpaceX.")
    parser.add_argument("--id", help="ID запуска SpaceX. Если не указан, скачиваются фото с последнего запуска.")
    args = parser.parse_args()
    fetch_spacex_images(launch_id=args.id)
