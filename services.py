import requests
import os
from dotenv import load_dotenv
from typing import Dict, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BudaService:
    load_dotenv()
    BASE_URL = os.getenv("BUDA_API_URL")

    @staticmethod
    def get_market_price(crypto: str, fiat: str) -> float:
        market_id = f"{crypto}-{fiat}".lower()
        url = f"{BudaService.BASE_URL}/{market_id}/ticker"
        
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            price = float(data['ticker']['last_price'][0])
            return price
        except requests.exceptions.HTTPError as e:
            logger.warning(f"Market {market_id} lookup failed: {e}")
            return 0.0
        except Exception as e:
            logger.error(f"Error fetching price for {market_id}: {e}")
            return 0.0

    @staticmethod
    def calculate_portafolio_value(portafolio: Dict[str, float], fiat: str) -> Tuple[float, Dict[str, float]]:
        total_value = 0.0
        breakdown = {}

        for crypto, amount in portafolio.items():
            crypto_upper = crypto.upper()
            
            if crypto_upper == fiat.upper():
                val = amount
            else:
                price = BudaService.get_market_price(crypto, fiat)
                val = price * amount
            
            breakdown[crypto_upper] = val
            total_value += val
            
        return total_value, breakdown
