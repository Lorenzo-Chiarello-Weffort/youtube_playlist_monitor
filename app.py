from flask import Flask, render_template, jsonify, redirect
import requests
from datetime import datetime, timedelta
import time

app = Flask(__name__)

# Variáveis globais para acompanhar o estado
last_access_time = None
next_access_time = None
time_remaining = None
last_time_checked = None

TIMEZONE = "America/Sao_Paulo"
URL_TO_ACCESS = "https://youtube-monitor.onrender.com"


@app.route('/access_url')
def access_url():
    global last_access_time, next_access_time, time_remaining, last_time_checked

    now = datetime.now()
    last_time_checked = now

    # Realiza o acesso à URL
    try:
        requests.get(URL_TO_ACCESS)
        last_access_time = now
        print(f"Acesso realizado em {last_access_time}")
    except Exception as e:
        print(f"Erro ao acessar a URL: {e}")

    # Calcula o próximo horário de acesso (00:00:10 do dia seguinte)
    next_day = now.date() + timedelta(days=1)
    next_access_time = datetime.combine(next_day, datetime.min.time()) + timedelta(seconds=10)

    # Calcula o tempo restante para o próximo acesso
    # time_remaining = (next_access_time - now).total_seconds()
    time_remaining = 60

    # Redireciona para a página principal
    return redirect('/index')


@app.route('/index')
def index():
    return render_template("index.html",
                           last_access_time=last_access_time,
                           next_access_time=next_access_time,
                           time_remaining=time_remaining,
                           last_time_checked=last_time_checked)

@app.route('/')
def main():
    return "<h1>Página inicial</h1> <br/> <h2>Rotas:</h2> <h3>/access_url</h3> <h3>/index</h3>"

if __name__ == "__main__":
    app.run(debug=True)
