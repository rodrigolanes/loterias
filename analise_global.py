from pymongo import MongoClient
import os
import sys
from datetime import datetime
import collections
import functools
import operator
from dotenv import load_dotenv


def gera_analise_espacial(resultados):

    dados = {"pares": 0,
             "impares": 0,
             "numeros": {},
             "dezenas": {'0': 0, '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0},
             "quadrantes": {'1': 0, '2': 0, '3': 0, '4': 0},
             "linhas": {'0': 0, '1': 0, '2': 0, '3': 0, '4': 0, '5': 0}}

    for resultado in resultados:

        dados["pares"] += resultado["dados"]["pares"]
        dados["impares"] += resultado["dados"]["impares"]
        dados["numeros"] = dict(functools.reduce(operator.add,
                                                 map(collections.Counter, [dados["numeros"], resultado["dados"]["numeros"]])))
        dados["dezenas"] = dict(functools.reduce(operator.add,
                                                 map(collections.Counter, [dados["dezenas"], resultado["dados"]["dezenas"]])))
        dados["quadrantes"] = dict(functools.reduce(operator.add,
                                                    map(collections.Counter, [dados["quadrantes"], resultado["dados"]["quadrantes"]])))
        dados["linhas"] = dict(functools.reduce(operator.add,
                                                map(collections.Counter, [dados["linhas"], resultado["dados"]["linhas"]])))
    return dados


if __name__ == '__main__':
    load_dotenv()

    urlConnection = os.getenv("URL_CONNECTION_LOTERIAS")

    client = MongoClient(urlConnection)

    db = client.loterias

    resultados = list(db.megasena_analisada.find({}).sort([("concurso", 1)]))

    analises = {
        "data": datetime.timestamp(datetime.now()),
        "analise_espacial_global": gera_analise_espacial(resultados),
        "analise_espacial_ultimos_10": gera_analise_espacial(resultados[-10:]),
        "analise_espacial_ultimos_20": gera_analise_espacial(resultados[-20:]),
        "analise_espacial_ultimos_50": gera_analise_espacial(resultados[-50:]),
        "analise_espacial_ultimos_100": gera_analise_espacial(resultados[-100:]),
        "analise_espacial_ultimos_500": gera_analise_espacial(resultados[-500:]),
        "analise_espacial_ultimos_1000": gera_analise_espacial(resultados[-1000:])
    }

    db.megasena_consolidado.insert_one(analises)

    # print(dados)
    # print({k: v for k, v in sorted(dados['numeros'].items(), key=lambda item: item[1])})
    # print({k: v for k, v in sorted(dados['numeros'].items())})

    # numeros = ({int(k): v for k, v in
    #            dados['numeros'].items()})

    # print({k: v for k, v in sorted(
    #    numeros.items())})
