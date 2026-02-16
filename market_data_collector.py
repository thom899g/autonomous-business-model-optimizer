import requests
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class MarketDataCollector:
    """
    Collects real-time market data from various sources using APIs.
    Implements error handling and retry mechanisms for robust data collection.
    """

    def __init__(self, api_keys: Dict[str, str]):
        self.api_keys = api_keys
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_keys["ALPHA_VANTAGE"]}'
        }

    def fetch_data(self, endpoint: str) -> Optional[Dict]:
        """
        Fetches data from the specified API endpoint with retry logic.
        
        Args:
            endpoint (str): The API endpoint to fetch data from.
            
        Returns:
            Dict or None: The fetched data as a dictionary or None if failed.
        """
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.get(endpoint, headers=self.headers)
                if response.status_code == 200:
                    return response.json()
                logger.warning(f"Attempt {attempt + 1} failed with status code: {response.status_code}")
            except Exception as e:
                logger.error(f"Exception occurred during data fetch: {str(e)}")
        return None

    def process_data(self, raw_data: Dict) -> Dict:
        """
        Processes and transforms raw market data into a structured format.
        
        Args:
            raw_data (Dict): The raw data returned from the API.
            
        Returns:
            Dict: Processed data in a usable format.
        """
        processed = {}
        try:
            if 'data' in raw_data:
                # Example processing: extract relevant fields
                processed['symbol'] = raw_data['data']['symbol']
                processed['price'] = raw_data['data']['price']
                # Add more processing logic as needed
            return processed
        except KeyError:
            logger.error("Invalid data structure received.")
            return {}

    def collect(self, symbols: list) -> Dict[str, Dict]:
        """
        Collects market data for a list of financial symbols.
        
        Args:
            symbols (list): List of financial symbols to collect data for.
            
        Returns:
            Dict[str, Dict]: Mapping of symbol to its collected data.
        """
        data = {}
        for symbol in symbols:
            endpoint = f"https://api.example.com/{symbol}"
            raw_data = self.fetch_data(endpoint)
            processed = self.process_data(raw_data)
            if processed:
                data[symbol] = processed
        return data

# Example usage:
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    api_keys = {
        "ALPHA_VANTAGE": os.getenv("ALPHA_VANTAGE_API_KEY"),
        # Add other API keys as needed
    }
    
    collector = MarketDataCollector(api_keys)
    symbols = ['AAPL', 'GOOGL']
    market_data = collector.collect(symbols)
    logger.info(f"Market data collected: {market_data}")