import argparse
import os
import requests
from main import create_folder, download_image
from dotenv import load_dotenv

load_dotenv()

NASA_API_KEY = os.getenv("NASA_API_KEY")

def fetch_epic_images(max_photos=10, folder_name="nasa_epic_images"):
    create_folder(folder_name)
    url = f"https://api.nasa.gov/EPIC/api/natural/images?api_key={NASA_API_KEY}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        for i, item in enumerate(data[:max_photos], start=1):
            date = item["date"].split(" ")[0]
            year, month, day = date.split("-")
            image_name = item["image"]
            image_url = f"https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{image_name}.png?api_key={NASA_API_KEY}"
            file_name = os.path.join(folder_name, f"epic_image_{i}.png")
            download_image(image_url, file_name)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к NASA EPIC API: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Скачивание фотографий NASA EPIC.")
    parser.add_argument("--max_photos", type=int, default=10, help="Максимальное количество фотографий.")
    args = parser.parse_args()
    fetch_epic_images(max_photos=args.max_photos)
