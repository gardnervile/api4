import argparse
import os
import requests
from utils import create_folder, download_image
from dotenv import load_dotenv
from datetime import datetime
from urllib.parse import urlencode


def fetch_epic_images(max_photos=10, folder_name="nasa_epic_images"):
    NASA_API_KEY = os.environ["NASA_API_KEY"]
    create_folder(folder_name)
    
    base_url = "https://api.nasa.gov/EPIC/api/natural/images"
    params = {"api_key": NASA_API_KEY}

    try:
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
                print(f"Ошибка при парсинге даты {date_str}: {e}")
                continue 

            image_name = item["image"]
            image_url = f"https://api.nasa.gov/EPIC/archive/natural/{year}/{month:02}/{day:02}/png/{image_name}.png"
            image_url_with_params = f"{image_url}?{urlencode(params)}"
            
            file_name = os.path.join(folder_name, f"epic_image_{i}.png")
            download_image(image_url_with_params, file_name)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к NASA EPIC API: {e}")

if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser(description="Скачивание фотографий NASA EPIC.")
    parser.add_argument("--max_photos", type=int, default=10, help="Максимальное количество фотографий.")
    args = parser.parse_args()
    fetch_epic_images(max_photos=args.max_photos)
