import argparse
import os
import requests
from utils import create_folder, download_image
from dotenv import load_dotenv
from datetime import datetime


def fetch_epic_images(api_key, max_photos=10, folder_name="nasa_epic_images"):
    create_folder(folder_name)
    
    base_url = "https://api.nasa.gov/EPIC/api/natural/images"
    params = {"api_key": api_key}
    
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    
    data = response.json()
    for i, item in enumerate(data[:max_photos], start=1):
        date_str = item["date"].split(" ")[0]
        try:
            date_obj = datetime.fromisoformat(date_str)
            year = date_obj.year
            month = date_obj.month
            day = date_obj.day
        except ValueError as e:
            raise ValueError(f"Ошибка при парсинге даты {date_str}: {e}") from e

        image_name = item["image"]
        image_url = f"https://api.nasa.gov/EPIC/archive/natural/{year}/{month:02}/{day:02}/png/{image_name}.png"
        
        file_name = os.path.join(folder_name, f"epic_image_{i}.png")
        download_image(image_url, file_name)


if __name__ == "__main__":
    load_dotenv()
    nasa_api_key = os.environ["NASA_API_KEY"]

    parser = argparse.ArgumentParser(description="Скачивание фотографий NASA EPIC.")
    parser.add_argument("--max_photos", type=int, default=10, help="Максимальное количество фотографий.")
    parser.add_argument("--folder_name", type=str, default="nasa_epic_images", help="Директория для сохранения изображений.")
    args = parser.parse_args()
    
    try:
        fetch_epic_images(api_key=nasa_api_key, max_photos=args.max_photos, folder_name=args.folder_name)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к NASA EPIC API: {e}")
    except ValueError as e:
        print(f"Ошибка при обработке данных: {e}")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
