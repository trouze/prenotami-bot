from prenotami import PrenotamiBot
from config import config
from argparse import ArgumentParser

if __name__ == "__main__":
    argparse = ArgumentParser("Prenotami-Bot")
    argparse.add_argument("--headless", type=bool, default=False, help="Execute in headless mode")
    args = argparse.parse_args()

    bot = PrenotamiBot(config, args.headless)
    bot.login()
    bot.check_appointments()