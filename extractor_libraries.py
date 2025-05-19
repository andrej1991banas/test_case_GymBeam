import requests
import json
import csv
import logging
from typing import Dict, List, Any
from datetime import datetime



# Nastavení logování
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GolemioExtractor:
    def __init__(self, config_path: str):
        """Inicializace extraktoru s cestou ke konfiguračnímu souboru."""
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        self.api_key = self.config.get('api_key')
        self.endpoint = self.config.get('api_endpoint')
        self.params = self.config.get('params', {})
        self.fields = self.config.get('fields', [])
        self.output_format = self.config.get('output_format', 'json')
        self.output_file = self.config.get('output_file', 'libraries.csv')
        self.headers = {
            'X-Access-Token': self.api_key,
            'Content-Type': 'application/json'
        }

    def fetch_data(self) -> List[Dict[str, Any]]:
        """Odešle požadavek na API a vrátí extrahovaná data."""
        all_data = []
        offset = self.params.get('offset', 0)
        limit = self.params.get('limit', 10)
        timeout = self.config.get('timeout', 10)  # Configurable timeout

        while True:
            self.params['offset'] = offset
            try:
                response = requests.get(self.endpoint, headers=self.headers, params=self.params, timeout=timeout)
                response.raise_for_status()
                data = response.json()

                results = []
                if data.get('type') == 'FeatureCollection':
                    for feature in data.get('features', []):
                        properties = feature.get('properties', {})
                        geometry = feature.get('geometry', {}).get('coordinates', [0, 0])

                        result = {
                            'id': properties.get('id', ''),
                            'name': properties.get('name', ''),
                            'street_address': properties.get('address', {}).get('street_address', ''),
                            'postal_code': properties.get('address', {}).get('postal_code', ''),
                            'address_locality': properties.get('address', {}).get('address_locality', ''),
                            'district': properties.get('district', ''),
                            'address_country': properties.get('address', {}).get('address_country', ''),
                            'latitude': geometry[1] if len(geometry) > 1 else 0,
                            'longitude': geometry[0] if len(geometry) > 0 else 0,
                        }

                        # Get current day of the week
                        today = datetime.now().strftime("%A")  # e.g., "Monday"

                        # Process opening hours
                        opening_hours = properties.get('opening_hours', [])
                        today_hours = next(
                            (oh for oh in opening_hours if
                             oh.get('day_of_week') == today and oh.get('is_default', False)), None
                        )

                        if today_hours:
                            result['opening_time'] = today_hours.get('opens', 'Zavřeno')
                        else:
                            result['opening_time'] = 'Zavřeno'


                        results.append(result)

                else:
                    # Handle single feature
                    properties = data.get('properties', {})
                    geometry = data.get('geometry', {}).get('coordinates', [0, 0])
                    result = {
                        'id': properties.get('id', ''),
                        'name': properties.get('name', ''),
                        'street_address': properties.get('address', {}).get('street_address', ''),
                        'postal_code': properties.get('address', {}).get('postal_code', ''),
                        'address_locality': properties.get('address', {}).get('address_locality', ''),
                        'district': properties.get('district', ''),
                        'address_country': properties.get('address', {}).get('address_country', ''),
                        'latitude': geometry[1] if len(geometry) > 1 else 0,
                        'longitude': geometry[0] if len(geometry) > 0 else 0,
                    }

                    # Get current day of the week
                    today = datetime.now().strftime("%A")

                    # Process opening hours
                    opening_hours = properties.get('opening_hours', [])
                    today_hours = next(
                        (oh for oh in opening_hours if oh.get('day_of_week') == today and oh.get('is_default', False)),
                        None
                    )

                    if today_hours:
                        result['opening_time'] = today_hours.get('opens', 'Zavřeno')
                    else:
                        result['opening_time'] = 'Zavřeno'

                    results.append(result)

                all_data.extend(results)
                logging.info(f"Načteno {len(results)} záznamů, offset: {offset}")

                if len(results) < limit:
                    logging.info("Žádná další data k načtení.")
                    break

                offset += limit

            except requests.exceptions.HTTPError as http_err:
                logging.error(f"HTTP chyba: {http_err}")
                if response.status_code == 429:
                    logging.error("Příliš mnoho požadavků. Čekám 60 sekund.")
                    import time
                    time.sleep(60)
                    continue
                break
            except requests.exceptions.RequestException as err:
                logging.error(f"Chyba požadavku: {err}")
                break
            except Exception as e:
                logging.error(f"Neočekávaná chyba: {e}")
                break

        return all_data

    def save_data(self, data: List[Dict[str, Any]]):
        """Uloží extrahovaná data do zvoleného formátu."""
        if self.output_format == 'json':
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logging.info(f"Data uložena do {self.output_file}")
        elif self.output_format == 'csv':
            if data:
                with open(self.output_file, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=self.fields)
                    writer.writeheader()
                    writer.writerows(data)
                logging.info(f"Data uložena do {self.output_file}")
        else:
            logging.warning(f"Nepodporovaný formát: {self.output_format}")

    def run(self):
        """Spustí proces extrakce a uložení dat."""
        logging.info("Spouštím extrakci dat...")
        data = self.fetch_data()
        if data:
            self.save_data(data)
        else:
            logging.warning("Žádná data k uložení.")

