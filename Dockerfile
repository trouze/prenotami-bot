FROM selenium/standalone-chrome
USER root
RUN apt -y update && apt -y upgrade && apt -y dist-upgrade
RUN apt --fix-broken install
RUN apt-get install -y python3 pip

COPY ./requirements.txt /opt/prenotami-bot/requirements.txt
COPY ./src /opt/prenotami-bot/src

WORKDIR /opt/prenotami-bot
RUN pip install -r requirements.txt

USER seluser
CMD ["python3","./src/main.py"]


