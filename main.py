import requests
import itertools
import sqlite3
from datetime import datetime, timedelta

from config import *
from airports import EU_AIRPORTS


def gerar_datas(inicio, fim):

    start = datetime.fromisoformat(inicio)
    end = datetime.fromisoformat(fim)

    datas = []

    while start <= end:
        datas.append(start.strftime("%Y-%m-%d"))
        start += timedelta(days=1)

    return datas


def enviar_telegram(msg):

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": msg
    })


def salvar_alerta(rota):

    conn = sqlite3.connect("deals.db")
    c = conn.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS deals(rota TEXT)")
    c.execute("INSERT INTO deals VALUES(?)", (rota,))

    conn.commit()
    conn.close()


def alerta_existe(rota):

    conn = sqlite3.connect("deals.db")
    c = conn.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS deals(rota TEXT)")
    c.execute("SELECT * FROM deals WHERE rota=?", (rota,))

    r = c.fetchone()

    conn.close()

    return r


def buscar_voo(origem, destino, ida, volta):

    # Simulação de preço (depois podemos conectar APIs reais)
    preco = 2000 + hash(origem + destino + ida) % 2000

    conexoes = 1

    return {
        "origem": origem,
        "destino": destino,
        "ida": ida,
        "volta": volta,
        "preco": preco,
        "conexoes": conexoes
    }


def main():

    idas = gerar_datas(DEPARTURE_START, DEPARTURE_END)
    voltas = gerar_datas(RETURN_START, RETURN_END)

    combos = list(itertools.product(idas, voltas, EU_AIRPORTS))

    voos = []

    for ida, volta, destino in combos[:800]:

        voo = buscar_voo(ORIGIN, destino, ida, volta)

        if voo["conexoes"] <= MAX_STOPS:
            voos.append(voo)

    # remover duplicados
    vistos = set()
    filtrados = []

    for v in voos:

        chave = (v["origem"], v["destino"], v["ida"], v["volta"])

        if chave not in vistos:
            vistos.add(chave)
            filtrados.append(v)

    for v in filtrados:

        if v["preco"] < MAX_PRICE_ALERT:

            rota = f"{v['origem']}-{v['destino']}-{v['ida']}-{v['volta']}"

            if not alerta_existe(rota):

                msg = f"""
🔥 PASSAGEM BARATA

{v['origem']} → {v['destino']}

💰 R${v['preco']}

🛫 {v['ida']}
🛬 {v['volta']}
"""

                enviar_telegram(msg)

                salvar_alerta(rota)


if __name__ == "__main__":
    main()
