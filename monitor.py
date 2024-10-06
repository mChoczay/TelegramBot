import ccxt.async_support as ccxt
import asyncio
import logging
import sys

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CryptoMonitor:
    def __init__(self, crypto_pairs):
        self.crypto_pairs = crypto_pairs
        self.exchange = ccxt.binance()  

    async def fetch_price(self, crypto_pair, timeout=10):
        try:
            return await asyncio.wait_for(self.exchange.fetch_ticker(crypto_pair), timeout)
        except asyncio.TimeoutError:
            logger.error(f"Timeout fetching price for {crypto_pair}")
            return None

    async def monitor_pair(self, crypto_pair):
        while True:
            try:
                ticker = await self.fetch_price(crypto_pair)
                if ticker:
                    price = ticker['last']
                    logger.info(f'Price for {crypto_pair}: {price}')
                    yield price 
            except Exception as e:
                logger.error(f"Error for {crypto_pair}: {e}")
            
            await asyncio.sleep(10) 

    async def close(self):
        await self.exchange.close()