import argparse
import os
import requests
from utils import create_folder, download_image, get_file_extension
from dotenv import load_dotenv


def fetch_apod_images(api_key, count=30, folder_name="nasa_apod_images"):
    create_folder(folder_name)
    url = "https://api.nasa.gov/planetary/apod"
    params = {"api_key": api_key, "count": count}
    
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
    nasa_api_key = os.getenv("NASA_API_KEY")

    if not nasa_api_key:
        print("Ошибка: NASA_API_KEY не найден. Убедитесь, что .env файл содержит ключ.")
        exit(1)

    parser = argparse.ArgumentParser(description="Скачивание фотографий NASA APOD.")
    parser.add_argument("--count", type=int, default=30, help="Количество фотографий для скачивания.")
    parser.add_argument("--folder_name", type=str, default="nasa_apod_images", help="Папка для сохранения изображений.")
    args = parser.parse_args()

    try:
        fetch_apod_images(api_key=nasa_api_key, count=args.count, folder_name=args.folder_name)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к NASA APOD API: {e}")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
