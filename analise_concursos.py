from pymongo import MongoClient
import os
import sys
from datetime import datetime
from dotenv import load_dotenv


def analisa_resultado(resultado):
    dados = {"pares": 0,
             "impares": 0,
             "numeros": {},
             "dezenas": {'0': 0, '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0},
             "quadrantes": {'1': 0, '2': 0, '3': 0, '4': 0},
             "linhas": {'0': 0, '1': 0, '2': 0, '3': 0, '4': 0, '5': 0}}
    for numero_str in resultado:
        numero = int(numero_str)
        if numero % 2 == 0:
            dados['pares'] += 1
        else:
            dados['impares'] += 1

        dados['numeros'][str(numero)] = dados['numeros'].get(numero, 0) + 1

        dados['dezenas'][str((numero // 10) % 10)] += 1

        if numero <= 10:
            dados['linhas']['0'] += 1
        elif numero <= 20:
            dados['linhas']['1'] += 1
        elif numero <= 30:
            dados['linhas']['2'] += 1
        elif numero <= 40:
            dados['linhas']['3'] += 1
        elif numero <= 50:
            dados['linhas']['4'] += 1
        else:
            dados['linhas']['5'] += 1

        if (numero >= 1 and numero <= 5) or (numero >= 11 and numero <= 15) or (numero >= 21 and numero <= 25):
            dados['quadrantes']['1'] += 1
        elif (numero >= 6 and numero <= 10) or (numero >= 16 and numero <= 20) or (numero >= 26 and numero <= 30):
            dados['quadrantes']['2'] += 1
        elif (numero >= 31 and numero <= 35) or (numero >= 41 and numero <= 45) or (numero >= 51 and numero <= 55):
            dados['quadrantes']['3'] += 1
        else:
            dados['quadrantes']['4'] += 1

    return dados


def analise_ganhadores(ganhadores):
    dados = {}
    for ganhador in ganhadores:
        uf = ganhador["sgUf"]
        dados[uf] = dados.get(uf, {"cidades": {}})
        cidades = dados[uf]["cidades"]

        nome_cidade = ganhador["noCidade"]

        cidade = cidades.get(nome_cidade, {"quantidade": 0})

        cidade["quantidade"] += 1

        cidades[nome_cidade] = cidade

        dados[uf]["ganhadores"] = ganhador["qtGanhadores"]


def analisa(db):
    print("Analisa Concursos")
    megasena = db.megasena
    megasena_analisada = db.megasena_analisada

    resultados = megasena.find({}).sort([("concurso", 1)])

    analises = []

    for resultado in resultados:
        analise = {}

        analise['concurso'] = resultado['concurso']
        timestamp_resultado = resultado['data']
        analise['data'] = timestamp_resultado
        data_resultado = datetime.fromtimestamp(timestamp_resultado/1000.0)
        analise['ano'] = data_resultado.strftime("%Y")
        analise['mes'] = data_resultado.strftime("%m")
        analise['dia'] = data_resultado.strftime("%d")
        analise['valor_arrecadado'] = resultado['vr_arrecadado']
        analise['resultado'] = [
            int(x) for x in resultado['resultadoOrdenado'].split("-")]
        analise['sena'] = {
            "ganhadores": resultado['ganhadores'], "valor": resultado['valor']}
        analise['quina'] = {
            "ganhadores": resultado['ganhadores_quina'], "valor": resultado['valor_quina']}
        analise['quadra'] = {
            "ganhadores": resultado['ganhadores_quadra'], "valor": resultado['valor_quadra']}
        analise['acumulou'] = resultado['sorteioAcumulado']
        analise['valor_acumulado'] = resultado['valor_acumulado']
        analise['valir_acumulado_final_zero_cinco'] = resultado['ac_final_zero']
        analise['valor_acumulado_especial'] = resultado['vr_acumulado_especial']
        analise['concurso_especial'] = True if resultado['concursoEspecial'] == 1 else False
        analise['estimativa_proximo_concurso'] = resultado['vr_estimativa']

        analise['dados'] = analisa_resultado(analise['resultado'])
        if not analise['acumulou'] and resultado['ganhadoresPorUf'] != None:
            analise['ganhadores'] = analise_ganhadores(
                resultado['ganhadoresPorUf'])
        analises.append(analise)

    db.drop_collection("megasena_analisada")
    megasena_analisada.insert_many(analises)


if __name__ == '__main__':
    load_dotenv()

    urlConnection = os.getenv("URL_CONNECTION_LOTERIAS")

    client = MongoClient(urlConnection)

    db = client.loterias

    analisa(db)
