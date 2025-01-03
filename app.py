from flask import Flask, render_template, jsonify, redirect
import requests
from datetime import datetime, timedelta, time
import pytz

app = Flask(__name__)

last_access_time = None
next_access_time = None
time_remaining = None
last_time_checked = None

TIMEZONE = pytz.timezone("America/Sao_Paulo")
# URL_TO_ACCESS = "https://youtube-monitor.onrender.com"
URL_TO_ACCESS = "https://google.com"

HOUR_TO_ACCESS = 20  # 0-23
MINUTES_TO_ACCESS = 20  # 0-59
# SECONDS_TO_ACCESS = 10 - Fixed

@app.route('/access_url')
def access_url():
    global last_access_time, next_access_time, time_remaining, last_time_checked

    now = datetime.now(TIMEZONE)
    last_time_checked = now

    try:
        requests.get(URL_TO_ACCESS)
        last_access_time = now
        print(f"Acesso realizado à {URL_TO_ACCESS} em {last_access_time}")
    except Exception as e:
        print(f"Erro ao acessar a URL: {e}")

    # Calcula o próximo horário de acesso considerando a hora e os minutos
    next_day = (now + timedelta(days=1)).date()
    next_access_time = datetime.combine(next_day, time(hour=HOUR_TO_ACCESS, minute=MINUTES_TO_ACCESS), tzinfo=TIMEZONE) + timedelta(seconds=10)

    # Calcula o tempo restante para o próximo acesso
    time_remaining = (next_access_time - now).total_seconds()

    # Redireciona para a página principal
    return redirect('/index')

@app.route('/index')
def index():
    return render_template("index.html",
                           last_access_time=last_access_time,
                           next_access_time=next_access_time,
                           time_remaining=time_remaining,
                           last_time_checked=last_time_checked)

@app.route('/load_test')
def load_test():
    global time_remaining
    time_remaining = 10

    return redirect('/index')

@app.route('/')
def main():
    return "<h1>Página inicial</h1> <br/> <h2>Rotas:</h2> <h3>/load_test - Carrega index com 60 segundos</h3> <h3>/access_url - Executa a operação de acessar url</h3> <h3>/index - Mostra as informações</h3>"

if __name__ == "__main__":
    app.run(debug=True)
