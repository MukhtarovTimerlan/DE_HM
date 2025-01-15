import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pandas as pd
import time
from prefect import get_run_logger


BASE_URL = "https://www.avito.ru"
ua = UserAgent()


def get_listing_links(main_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(main_url, headers=headers)
    if response.status_code != 200:
        print(f"Ошибка: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    links = []
    for item in soup.find_all("a", {"itemprop": "url", "data-marker": "item-title"}):
        href = item.get("href")
        if href and not href.startswith("http"):
            links.append(BASE_URL + href)
    return links


def get_listing_data(listing_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(listing_url, headers=headers)
    if response.status_code != 200:
        print(f"Ошибка: {response.status_code}")
        return {}

    soup = BeautifulSoup(response.text, "html.parser")

    try:
        number_of_rooms = soup.find("li", text=lambda t: t and "Количество комнат" in t).text.split(":")[-1].strip()
        total_area = soup.find("li", text=lambda t: t and "Общая площадь" in t).text.split(":")[-1].strip()
        living_area = soup.find("li", text=lambda t: t and "Жилая площадь" in t).text.split(":")[-1].strip()
        floor_info = soup.find("li", text=lambda t: t and "Этаж" in t).text.split(":")[-1].strip()
        floor, number_of_floors = map(str.strip, floor_info.split("из"))
        ceiling_height = soup.find("li", text=lambda t: t and "Высота потолков" in t).text.split(":")[-1].strip()
        construction_year = soup.find("li", text=lambda t: t and "Год постройки" in t).text.split(":")[-1].strip()

        min_to_metro = soup.find("span",
                                 class_="style-item-address-georeferences-item-interval__container-HBqQL").text.strip()

        property_data = {
            "number_of_rooms": number_of_rooms,
            "total_area": total_area,
            "living_area": living_area,
            "floor": floor,
            "number_of_floors": number_of_floors,
            "ceiling_height": ceiling_height,
            "construction_year": construction_year,
            "min_to_metro": min_to_metro,
        }
        for key, value in property_data.items():
            print(f"{key}: {value}")

    except AttributeError as e:
        print(f"Ошибка парсинга: {e}")
    return property_data


def collect_data():
    logger = get_run_logger()
    url = "https://www.avito.ru/moskva/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1&context=H4sIAAAAAAAA_0RSTXebMBD8L772EEHiOJBTKoIKFUpEYpB0A0EwqrBT8yFIX_97n4jzetq3erOzM6MtfNf_0_sO8DfydD7XcmhPx8197293rr-JjoOMulBVSE-lNu2TNq3sMlOiUInMtDg0rWAH24-cpe-lu5WRepfRAF8An2hfoQeAAzpVCEcEPQKs6OihBHCcNgRhDIO0qeA3gHdpM8AFYJY2A_oOOKb9gALAd2lbwRuA9w3Ab7Qn8ArwgE4rJmnM74mOFoev6EgQBNw0AJ9pP0ADeGA5b9Z693OH9adeieYDd7NB5FvAYHTLYNyKfJ4q5-IHZR9FXo1Zly3S_e-77LylzMMe52EvWGxnewbjvsi3Z-lYzLBjMF4ECx3ByMpdO6aVLNPyqL9yuQX8mU6e1YVTBQM6rr4DmwcEWNkaXLgVZ6kWrrfUe_1o-RJF152lSw7rn_z6fCcquSaKmk9_4cJz5-Nrf6Ie5nX29cFN4CwjtTckNO2T2i_kVXhvL7OMjqmuf6RfGmub_0SgA_D1JddZRu0so87RFTpMIrzcgpsdZEdO7DrWAulF5NZ37DEGWntEd_7m7Xzqnoumtu3O38hiKPSp2dz__RcAAP__7YCuinoCAAA&user=1"
    try:
        listing_links = get_listing_links(url)
        all_data = []
        for link in listing_links:
            print(f"Парсим: {link}")
            data = get_listing_data(link)
            if data:
                all_data.append(data)
            time.sleep(10)
        df = pd.DataFrame(all_data)
        old_df = pd.read_csv('data/raw/moscow_flats_dataset.csv')
        fin_df = pd.concat([old_df, df])
        fin_df.to_csv('data/raw/moscow_flats_dataset.csv',index=False)
    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")



