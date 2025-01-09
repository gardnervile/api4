import argparse
import os
import requests
from main import create_folder, download_image, get_file_extension
from dotenv import load_dotenv

load_dotenv()

NASA_API_KEY = os.getenv("NASA_API_KEY")

def fetch_apod_images(count=30, folder_name="nasa_apod_images"):
    create_folder(folder_name)
    url = "https://api.nasa.gov/planetary/apod"
    params = {"api_key": NASA_API_KEY, "count": count}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        for i, item in enumerate(data, start=1):
            if "url" in item and item["url"].startswith("http"):
                file_name = f"apod_image_{i}{get_file_extension(item['url'])}"
                download_image(item["url"], os.path.join(folder_name, file_name))
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к NASA APOD API: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Скачивание фотографий NASA APOD.")
    parser.add_argument("--count", type=int, default=30, help="Количество фотографий для скачивания.")
    args = parser.parse_args()
    fetch_apod_images(count=args.count)
