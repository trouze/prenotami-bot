from prenotami import Prenotami
from config import config

if __name__ == "__main__":
    run = Prenotami(config)
    run.login()
    run.check_appointments()