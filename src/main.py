from prenotami import PrenotamiBot
from config import config

if __name__ == "__main__":
    bot = PrenotamiBot(config)
    bot.login()
    bot.check_appointments()