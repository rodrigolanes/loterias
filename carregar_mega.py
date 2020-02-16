import requests
from pymongo import MongoClient
import json
import sys
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    urlConnection = os.getenv("URL_CONNECTION_LOTERIAS")

    client = MongoClient(urlConnection)

    db = client.loterias

    megasena = db.megasena

    ultimo_concurso = megasena.find({}, {"concurso": 1}).sort([
        ("concurso", -1)]).limit(1)

    concurso = 0

    for ultimo in ultimo_concurso:
        concurso = ultimo['concurso']

    while True:
        concurso += 1

        url = f'http://loterias.caixa.gov.br/wps/portal/loterias/landing/megasena/!ut/p/a1/04_Sj9CPykssy0xPLMnMz0vMAfGjzOLNDH0MPAzcDbwMPI0sDBxNXAOMwrzCjA0sjIEKIoEKnN0dPUzMfQwMDEwsjAw8XZw8XMwtfQ0MPM2I02-AAzgaENIfrh-FqsQ9wNnUwNHfxcnSwBgIDUyhCvA5EawAjxsKckMjDDI9FQE-F4ca/dl5/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_HGK818G0KO6H80AU71KG7J0072/res/id=buscaResultado/c=cacheLevelPage/=/?timestampAjax=1581880457640&concurso={concurso}'

        req = requests.get(url)

        resultado = json.loads(req.content)

        if resultado['concurso'] == None:
            sys.exit()  # Concurso ainda não existe

        resultado['_id'] = concurso

        megasena.insert_one(resultado)

        print(concurso)

        if str(concurso) == resultado['proximoConcurso']:
            sys.exit()
