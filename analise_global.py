from pymongo import MongoClient
import os
import sys
from datetime import datetime
import collections
import functools
import operator
from dotenv import load_dotenv


def gera_analises_espaciais(megasena_analisada):
    resultados = megasena_analisada.find({}).sort([("concurso", 1)])

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

    print(dados)
    # print({k: v for k, v in sorted(dados['numeros'].items(), key=lambda item: item[1])})
    # print({k: v for k, v in sorted(dados['numeros'].items())})

    numeros = ({int(k): v for k, v in
                dados['numeros'].items()})

    print({k: v for k, v in sorted(
        numeros.items())})


def gera_series_temporais(megasena_analisada):
    pass


if __name__ == '__main__':
    load_dotenv()

    urlConnection = os.getenv("URL_CONNECTION_LOTERIAS")

    client = MongoClient(urlConnection)

    db = client.loterias

    analises = {
        "analises_espaciais": gera_analises_espaciais(db.megasena_analisada),
        "series_temporais": gera_series_temporais(db.megasena_analisada)
    }
