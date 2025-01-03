import time
from datetime import datetime, timedelta
import requests
import logging

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Variáveis globais para acompanhar o estado
last_access_time = None
next_access_time = None
time_remaining = None

TIMEZONE = "America/Sao_Paulo"
URL_TO_ACCESS = "http://google.com"

def main():
    global last_access_time, next_access_time, time_remaining

    logging.info("Aplicação iniciada.")
    
    while True:
        logging.info("Executando checagem...")

        now = datetime.now()  # Mantido sem timezone para evitar erros com TIMEZONE
        logging.info(f"Hora atual: {now}")

        # Calcula o próximo horário de acesso (00:00:10 do dia seguinte)
        if not next_access_time or now >= next_access_time:
            next_day = now.date() + timedelta(days=1)
            next_access_time = datetime.combine(next_day, datetime.min.time()) + timedelta(seconds=10)
            logging.info(f"Próximo horário de acesso definido: {next_access_time}")

        # Se passou do horário de acesso, realiza o acesso
        if now >= next_access_time:
            try:
                logging.info(f"Tentando acessar a URL: {URL_TO_ACCESS}")
                requests.get(URL_TO_ACCESS)
                last_access_time = datetime.now()
                logging.info(f"Acesso realizado com sucesso em {last_access_time}")
            except Exception as e:
                logging.error(f"Erro ao acessar a URL: {e}")

        # Calcula o tempo restante para o próximo acesso
        time_remaining = (next_access_time - datetime.now()).total_seconds()
        logging.info(f"Tempo restante para o próximo acesso: {time_remaining} segundos.")

        # Aguarda até o próximo acesso ou atualiza os valores em intervalos curtos
        # time.sleep(min(time_remaining, 60))
        time.sleep(10)

if __name__ == "__main__":
    main()
