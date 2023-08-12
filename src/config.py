from dotenv import load_dotenv
import os


load_dotenv()

config = {
    "email": {
        "username": os.getenv('EMAIL_USERNAME'),
        "password": os.getenv('EMAIL_PASSWORD'),
        "server": os.getenv('EMAIL_SERVER'),
        "recipient": os.getenv('EMAIL_RECIPIENT'),
        "sender": os.getenv('EMAIL_SENDER'),
    },
    "prenotami": {
        "username": os.getenv('PRENOTAMI_USERNAME'),
        "password": os.getenv('PRENOTAMI_PASSWORD')
    }
}