import locale
from datetime import datetime


def formata_concurso_text(concurso):
    texto = """{0} - {1}

{2}

{3} Senas - prêmio: {4}
{5} Quinas - prêmio: {6}
{7} Quadras - prêmio: {8}

Valor Acumulado: {9}

Previsão de Prêmio: *{10}*

Próximo Sorteio: {11}

Próximo Concurso 0 ou 5: {12}
Valor Acumulado 0 ou 5: {13}

Acumulado Mega da Virada: {14}"""

    data_concurso = datetime.fromtimestamp(concurso["data"]/1000.0)
    data_proximo_concurso = datetime.fromtimestamp(
        concurso["dt_proximo_concurso"]/1000.0)

    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    premio = valor = locale.currency(
        concurso["valor"], grouping=True, symbol=None)
    premio_quina = locale.currency(
        concurso["valor_quina"], grouping=True, symbol=None)
    premio_quadra = locale.currency(
        concurso["valor_quadra"], grouping=True, symbol=None)

    valor_acumulado = locale.currency(
        concurso["valor_acumulado"],
        grouping=True,
        symbol=None)

    valor_estimado = locale.currency(
        concurso["vr_estimativa"],
        grouping=True,
        symbol=None)

    valor_zero_cinco = locale.currency(
        concurso["ac_final_zero"],
        grouping=True,
        symbol=None)

    valor_mega_virada = locale.currency(
        concurso["vr_acumulado_especial"],
        grouping=True,
        symbol=None)

    if concurso["sorteioAcumulado"]:
        texto = "*Acumulou!!!*\n\n" + texto

    return texto.format(
        concurso["concurso"],
        data_concurso.strftime("%d/%m/%Y"),
        concurso["resultadoOrdenado"],
        concurso["ganhadores"],
        premio,
        concurso["ganhadores_quina"],
        premio_quina,
        concurso["ganhadores_quadra"],
        premio_quadra,
        valor_acumulado,
        valor_estimado,
        data_proximo_concurso.strftime("%d/%m/%Y"),
        concurso["prox_final_zero"],
        valor_zero_cinco,
        valor_mega_virada
    )


if __name__ == '__main__':
    concurso = {'proximoConcurso': '2294', 'concursoAnterior': '2293', 'forward': None, 'mensagens': [], 'concurso': 2294, 'data': 1598670000000, 'resultado': '09-43-20-41-33-15', 'ganhadores': 0, 'ganhadores_quina': 49, 'ganhadores_quadra': 5779, 'valor': 0.0, 'valor_quina': 85567.49, 'valor_quadra': 1036.46, 'acumulado': 1, 'valor_acumulado': 72530802.23, 'dtinclusao': 1598746440000, 'prox_final_zero': '2295', 'ac_final_zero': 72530802.23, 'proxConcursoFinal': None, 'observacao': None, 'rowguid': '8AEDC36A-6520-4307-B614-836073329F16',
                'ic_conferido': '1', 'de_local_sorteio': 'Espaço Loterias Caixa', 'no_cidade': 'SÃO PAULO', 'sg_uf': 'SP', 'vr_estimativa': 82000000.0, 'dt_proximo_concurso': 1599015600000, 'vr_acumulado_especial': 57593784.6, 'vr_arrecadado': 72721714.5, 'ic_concurso_especial': False, 'error': False, 'rateioProcessamento': False, 'sorteioAcumulado': True, 'concursoEspecial': '0', 'ganhadoresPorUf': None, 'resultadoOrdenado': '09-15-20-33-41-43', 'dataStr': '29/08/2020', 'dt_proximo_concursoStr': '02/09/2020'}
    print(formata_concurso_text(concurso))
