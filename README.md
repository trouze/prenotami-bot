# Prenotami Bot

Crawler that checks for availability of appointments for renewal of CIE (Carta d'Identità Elettronica)
on Italy's Ministry of Foreign Affairs site Prenot@mi.

## Usage

1. Create `.env` file with values as per [`env.sample`](./env.sample)
2. Build docker image
```bash
docker build . -t pviotti/prenotami-bot
```
3. Run docker container using the `.env` environment file
```bash
docker run --env-file .env pviotti/prenotami-bot:latest
```