import os
from dotenv import load_dotenv

load_dotenv()

def getenv(key: str) -> str:
    value = os.environ.get(key)
    if value is None:
        raise EnvironmentError('{} environmvet variable is missing'.format(key))
    return value

TOKEN = getenv('TELEGRAM_BOT_TOKEN')
CHANNEL_ID = int(getenv('ANAL_CHANNEL_ID'))
CHAT_ID = int(getenv('ANAL_CHAT_ID'))
API_KEY = getenv('GOOGLE_CLOUD_API_KEY')
API_ID = int(getenv('TELEGRAM_CLIENT_API_ID'))
API_HASH = getenv('TELEGRAM_CLIENT_API_HASH')

IDIOTS_ANSWERS = {
    int(getenv('GLEB_TELEGRAM_ID')): "Глеб, дебил блять, научись команды писать",
    int(getenv('ALEX_TELEGRAM_ID')): "ААААААААААААААААААА",
    int(getenv('EUGENE_TELEGRAM_ID')): "гав-гав >w<",
    int(getenv('IVAN_TELEGRAM_ID')): "идиот"
}