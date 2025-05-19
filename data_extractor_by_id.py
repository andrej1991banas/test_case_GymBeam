import requests
import json
import csv
import logging
from typing import Dict, List, Any
from datetime import datetime
import pandas as pd
import logging


# Nastavení logování
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GolemioExtractorId:
    def __init__(self, config_path: str):
        """Inicializace extraktoru s cestou ke konfiguračnímu souboru."""
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        self.api_key = self.config.get('api_key')
        self.endpoint = self.config.get('api_endpoint')
        self.id = self.config.get('library_id')
        self.fields = self.config.get('fields', [])
        self.output_format = self.config.get('output_format', 'json')
        self.output_file = self.config.get('output_file', 'output.json')
        self.headers = {
            'X-Access-Token': self.api_key,
            'Content-Type': 'application/json'
        }
        self.url = f"{self.endpoint}/{self.id}"

    def fetch_data(self) -> List[Dict[str, Any]]:
        """Odešle požadavek na API a vrátí extrahovaná data."""
        try:
            response = requests.get(url=self.url, headers=self.headers, timeout=10)
            response.raise_for_status()  # Vyvolá HTTPError pro neúspěšné požadavky

            # Parse JSON response
            data = response.json()
            # Extrakce dat podle self.fields
            result = {
                "id": data["properties"]["id"],
                "name": data["properties"]["name"],
                "street_address": data["properties"]["address"]["street_address"],
                "postal_code": data["properties"]["address"]["postal_code"],
                "address_locality": data["properties"]["address"]["address_locality"],
                "district": data["properties"]["district"],
                "address_country": data["properties"]["address"]["address_country"],
                "latitude": data["geometry"]["coordinates"][1],
                "longitude": data["geometry"]["coordinates"][0]
            }


            # Get current day of the week
            today = datetime.now().strftime("%A")  # e.g., "Monday"

            # Process opening hours
            opening_hours = data["properties"]["opening_hours"]
            today_hours = next(
                (oh for oh in opening_hours if oh["day_of_week"] == today), None
            )

            if today_hours:
                result["opening_day"] = today_hours["day_of_week"]
                result["opening_time"] = today_hours.get("opens", "Zavřeno")
                result["closing_time"] = today_hours.get("closes", "Zavřeno")

            else:
                result["opening_day"] = today
                result["opening_time"] = "Zavřeno"
                result["closing_time"] = "Zavřeno"
                logging.info(f"Knižnica je dnes ({result['opening_day']}) zavřená.")

            # Return the result wrapped in a list
            return [result]

        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP chyba: {http_err}")
            return []
        except requests.exceptions.RequestException as err:
            logging.error(f"Chyba při požadavku: {err}")
            return []
        except KeyError as key_err:
            logging.error(f"Chyba ve struktuře dat: {key_err}")
            return []

    def save_data(self, data: List[Dict[str, Any]]):
        """Uloží extrahovaná data do zvoleného formátu pomocí pandas."""
        if not data:
            logging.warning("Žádná data k uložení.")
            return

        try:
            df = pd.DataFrame(data)

            if self.output_format == 'json':
                df.to_json(self.output_file, orient='records', force_ascii=False, indent=2)
                logging.info(f"Data uložena do {self.output_file} ve formátu JSON.")
            elif self.output_format == 'csv':
                df.to_csv(self.output_file, index=False, encoding='utf-8')
                logging.info(f"Data uložena do {self.output_file} ve formátu CSV.")
            else:
                logging.warning(f"Nepodporovaný formát: {self.output_format}")

        except Exception as e:
            logging.error(f"Chyba při ukládání dat: {e}")

    def run(self):
        """Spustí proces extrakce a uložení dat."""
        logging.info("Spouštím extrakci dat...")
        data = self.fetch_data()
        self.save_data(data)