import json
import logging
import os
import sys
import time

import requests
from dotenv import load_dotenv
from pymongo import MongoClient
from telegram.ext import Updater

from analise_acumulada import analise_global
from analise_concursos import analisa
from utils.format import formata_concurso_text

load_dotenv()

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    urlConnection = os.getenv("URL_CONNECTION_LOTERIAS")
    telegram_token = os.getenv("TELEGRAM_TOKEN")
    owner_user_id = os.getenv("OWNER_USER_ID")

    client = MongoClient(urlConnection)

    db = client.loterias

    megasena = db.megasena

    ultimo_concurso = megasena.find({}, {"concurso": 1, "_id": 0}).sort([
        ("concurso", -1)]).limit(1)

    concurso = 0

    for ultimo in ultimo_concurso:
        ultimo_concurso = ultimo['concurso']

    concurso = ultimo_concurso - 2

    while True:
        concurso += 1

        url = f'http://loterias.caixa.gov.br/wps/portal/loterias/landing/megasena/!ut/p/a1/04_Sj9CPykssy0xPLMnMz0vMAfGjzOLNDH0MPAzcDbwMPI0sDBxNXAOMwrzCjA0sjIEKIoEKnN0dPUzMfQwMDEwsjAw8XZw8XMwtfQ0MPM2I02-AAzgaENIfrh-FqsQ9wNnUwNHfxcnSwBgIDUyhCvA5EawAjxsKckMjDDI9FQE-F4ca/dl5/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_HGK818G0KO6H80AU71KG7J0072/res/id=buscaResultado/c=cacheLevelPage/=/?timestampAjax=1581880457640&concurso={concurso}'

        req = requests.get(url)

        if req.status_code == 504:
            print("sleep 10s")
            time.sleep(10)
            req = requests.get(url)

        if req.status_code == 504:
            print("sleep 20s")
            time.sleep(20)
            req = requests.get(url)

        resultado = json.loads(req.content)

        if resultado['concurso'] == None:
            break  # Concurso ainda não existe

        megasena.update_one(
            {r"concurso": resultado["concurso"]}, {"$set": resultado}, upsert=True)

        print(concurso)

        # Quando no último concurso que aconteceu, tanto a variável concurso quando próximo concurso ficam com os números iguais.
        if str(concurso) == resultado['proximoConcurso'] and concurso > ultimo_concurso:
            updater = Updater(token=telegram_token, use_context=True)
            updater.bot.send_message(chat_id=owner_user_id, text=formata_concurso_text(
                resultado), parse_mode="MARKDOWN")
            updater.stop()

            analisa(db)
            analise_global(db)
            break
