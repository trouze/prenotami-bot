from dotenv import load_dotenv
import os
load_dotenv()

config = {
    "carriers": {
        "att": "@mms.att.net",
        "tmobile": "@tmomail.net",
        "verizon": "@vtext.com",
        "sprint": "@messaging.sprintpcs.com"
    },
    "phone_numbers": [
        {
            "dev": False,
            "carrier": "verizon",
            "number": os.getenv('phone_number_a')
        },
        {
            "dev": True,
            "carrier": "verizon",
            "number": os.getenv('phone_number_b')
        }
    ],
    "email": {
        "username": os.getenv('email'),
        "password": os.getenv('email_password')
    },
    "prenotami": {
        "username": os.getenv('prenotami_username'),
        "password": os.getenv('prenotami_password')
    }
}