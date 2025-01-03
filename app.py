from flask import Flask, render_template, jsonify
import threading
import time
from datetime import datetime, timedelta
import requests

app = Flask(__name__)

# Variáveis globais para acompanhar o estado
last_access_time = None
next_access_time = None
time_remaining = None
last_time_checked = None

TIMEZONE = "America/Sao_Paulo"
URL_TO_ACCESS = "http://google.com"


def scheduler():
    global last_access_time, next_access_time, time_remaining, last_time_checked

    while True:
        print("Executando checagem...")
        now = datetime.now(TIMEZONE)
        last_time_checked = now

        # Calcula o próximo horário de acesso (00:00:10 do dia seguinte)
        if not next_access_time or now >= next_access_time:
            next_day = now.date() + timedelta(days=1)
            next_access_time = datetime.combine(next_day, datetime.min.time(), tzinfo=TIMEZONE) + timedelta(seconds=10)

        # Se passou do horário de acesso, realiza o acesso
        if now >= next_access_time:
            try:
                requests.get(URL_TO_ACCESS)
                last_access_time = datetime.now(TIMEZONE)
                print(f"Acesso realizado em {last_access_time}")
            except Exception as e:
                print(f"Erro ao acessar a URL: {e}")

        # Calcula o tempo restante para o próximo acesso
        time_remaining = (next_access_time - datetime.now(TIMEZONE)).total_seconds()

        # Aguarda até o próximo acesso ou atualiza os valores em intervalos curtos
        # time.sleep(min(time_remaining, 60))
        time.sleep(10)


@app.route('/')
def index():
    return render_template("index.html",
                           last_access_time=last_access_time,
                           next_access_time=next_access_time,
                           time_remaining=time_remaining,
                           last_time_checked)


if __name__ == "__main__":
    # Inicia o scheduler em uma thread separada
    scheduler_thread = threading.Thread(target=scheduler, daemon=True)
    scheduler_thread.start()

    # Inicia o servidor Flask
    app.run(debug=True)
