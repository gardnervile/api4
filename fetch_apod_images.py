import argparse
import os
import requests
from utils import create_folder, download_image, get_file_extension
from dotenv import load_dotenv


def fetch_apod_images(count=30, folder_name="nasa_apod_images"):
    create_folder(folder_name)
    url = "https://api.nasa.gov/planetary/apod"
    params = {"api_key": NASA_API_KEY, "count": count}
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    for i, item in enumerate(data, start=1):
        if item.get("media_type") == "image" and "url" in item and item["url"].startswith("http"):
            file_name = f"apod_image_{i}{get_file_extension(item['url'])}"
            download_image(item["url"], os.path.join(folder_name, file_name))
        else:
            print(f"Пропущено: {item['title']} (тип: {item.get('media_type')})")

if __name__ == "__main__":
    load_dotenv()
    NASA_API_KEY = os.environ["NASA_API_KEY"]
    parser = argparse.ArgumentParser(description="Скачивание фотографий NASA APOD.")
    parser.add_argument("--count", type=int, default=30, help="Количество фотографий для скачивания.")
    args = parser.parse_args()

    try:
        fetch_apod_images(count=args.count)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к NASA APOD API: {e}")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
