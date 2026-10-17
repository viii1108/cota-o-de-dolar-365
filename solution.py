import requests
from datetime import datetime, timedelta


def cotar():
    hoje = datetime.now().date()
    datas = [hoje - timedelta(days=i) for i in range(365)]

    cotacoes = []
    cotacao_anterior = None

    # Percorre do dia mais antigo até hoje para preencher dias sem cotação.
    for dia in reversed(datas):
        data = dia.strftime("%m-%d-%Y")

        url = (
            "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
            "CotacaoDolarDia(dataCotacao=@dataCotacao)"
            f"?@dataCotacao='{data}'&$top=100&$format=json&$select=cotacaoCompra"
        )

        resposta = requests.get(url)
        resposta.raise_for_status()
        valores = resposta.json()["value"]

        if valores:
            cotacao_anterior = valores[0]["cotacaoCompra"]
        elif cotacao_anterior is None:
            # Se o primeiro dia do período não for útil, busca uma cotação anterior.
            dia_busca = dia - timedelta(days=1)

            while cotacao_anterior is None:
                data_busca = dia_busca.strftime("%m-%d-%Y")
                url_busca = (
                    "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
                    "CotacaoDolarDia(dataCotacao=@dataCotacao)"
                    f"?@dataCotacao='{data_busca}'&$top=100&$format=json&$select=cotacaoCompra"
                )

                resposta_busca = requests.get(url_busca)
                resposta_busca.raise_for_status()
                valores_busca = resposta_busca.json()["value"]

                if valores_busca:
                    cotacao_anterior = valores_busca[0]["cotacaoCompra"]
                else:
                    dia_busca -= timedelta(days=1)

        cotacoes.append(cotacao_anterior)

    # Retorna do dia mais recente para o mais antigo.
    return cotacoes[::-1]


if __name__ == "__main__":
    resultado = cotar()
    print(len(resultado), resultado)