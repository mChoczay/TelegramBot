import asyncio
import telebot
import logging
import threading
from monitor import CryptoMonitor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = ""
bot = telebot.TeleBot(TOKEN, threaded=True)  

THRESHOLD_VALUES = {
    'BTC/EUR': 20000, 
    'ETH/USD': 1500    
}

NOTIFICATION_SENT = {pair: False for pair in THRESHOLD_VALUES.keys()}

async def monitor_cryptos():
    crypto_pairs = list(THRESHOLD_VALUES.keys())
    monitor = CryptoMonitor(crypto_pairs)

    for pair in crypto_pairs:
        async for price in monitor.monitor_pair(pair):  
            threshold = THRESHOLD_VALUES[pair]

            if price < threshold and not NOTIFICATION_SENT[pair]:
                bot.send_message("@shirutest", f"Alert! {pair} is below {threshold}. Current value: {price}")
                NOTIFICATION_SENT[pair] = True 
            elif price >= threshold and NOTIFICATION_SENT[pair]:
                bot.send_message("@shirutest", f"Update: {pair} is back above the threshold. Current value: {price}")
                NOTIFICATION_SENT[pair] = False 
            else:
                bot.send_message("@shirutest", f"Update: {pair}. Current value: {price}")

    await monitor.close()  

def start_bot_polling():
    logger.info("Starting Telegram bot polling in a separate thread...")
    try:
        bot.infinity_polling()
    except Exception as e:
        logger.error(f"Error in polling: {e}")

async def run_bot():
    logger.info("Starting bot and monitoring...")

    polling_thread = threading.Thread(target=start_bot_polling)
    polling_thread.daemon = True
    polling_thread.start()

    await monitor_cryptos()

if __name__ == '__main__':
    asyncio.run(run_bot())