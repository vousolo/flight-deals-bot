import requests
import json

TELEGRAM_TOKEN = "SEU_TOKEN"
CHAT_ID = "SEU_CHAT_ID"

MAX_PRICE = 3200
MAX_RESULTS = 3

origem = "GRU"

destinos_ida = [
    "MAD",  # Madrid
    "MXP",  # Milão
    "BCN",  # Barcelona
    "LIS"   # Lisboa
]

destinos_volta = [
    "FCO",  # Roma
    "NAP",  # Napoli
    "PMO",  # Palermo
    "CTA"   # Catania
]


def gerar_link(origem, destino, ida, volta):
    return f"https://www.skyscanner.com/transport/flights/{origem}/{destino}/{ida}/{volta}"


def enviar_telegram(msg):

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": msg
    }

    requests.post(url, data=payload)


def buscar_voos():

    voos = []

    # EXEMPLO (simulado)
    voos.append({
        "origem": "GRU",
        "destino": "MAD",
        "preco": 2450,
        "ida": "22-08",
        "volta": "28-10",
        "conexoes": 1
    })

    voos.append({
        "origem": "GRU",
        "destino": "MXP",
        "preco": 2890,
        "ida": "25-08",
        "volta": "30-10",
        "conexoes": 1
    })

    return voos


def filtrar_voos(voos):

    voos_filtrados = []

    for voo in voos:

        if voo["preco"] > MAX_PRICE:
            continue

        if voo["conexoes"] > 1:
            continue

        voos_filtrados.append(voo)

    voos_filtrados.sort(key=lambda x: x["preco"])

    return voos_filtrados[:MAX_RESULTS]


def main():

    voos = buscar_voos()

    voos_filtrados = filtrar_voos(voos)

    for voo in voos_filtrados:

        link = gerar_link(
            voo["origem"],
            voo["destino"],
            voo["ida"],
            voo["volta"]
        )

        mensagem = f"""
✈️ Promoção encontrada

{voo['origem']} → {voo['destino']}

💰 R$ {voo['preco']}

📅 Ida: {voo['ida']}
📅 Volta: {voo['volta']}

🔌 {voo['conexoes']} conexão

🔗 Comprar:
{link}
"""

        enviar_telegram(mensagem)


if __name__ == "__main__":
    main()
