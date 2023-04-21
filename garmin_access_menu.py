#!/usr/bin/env python3
"""
pip3 install garminconnect
pip3 install cloudscraper requests readchar pwinput
"""
import datetime
import json
import logging
import os
import sys

import requests
import pwinput
import readchar

from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError
)

from json_readers import(
    hr_reader,
    steps_reader,
    resp_reader,
    spo2_reader,
    sleep_reader,
    week_steps_reader,
    body_battery_reader,
    stress_reader
)

from populateAIO import sendToAIO

from data.Heart_rate.feedback import feedback_hr
from data.Sleep.feedback import feedback_sleep
from data.Body_Battery.feedback import feedback_bodybattery
from data.Steps.feedback import feedback_day_steps

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

email = ''
password = ''
api = None
# Escolher dia do qual quer obter os dados
while True:
   try:
       dia = int(input('Introduza o dia que quer visualizar (0-hoje; 1-ontem; 2-há 2 dias;...): '))
       if dia >= 0:
           break
       else:
           print('Introduza um número válido.')
   except ValueError as e:
       print('Introduza um número válido')

today = datetime.date.today() - datetime.timedelta(days=dia)
startdate = today - datetime.timedelta(days=7) # Selecionar a última semana

menu_options = {
    "1": f"Resumo do dia em '{today.isoformat()}'",
    "2": f"Informação estatística e composição corporal em '{today.isoformat()}'", # Composição corporal inexistente porque não registo peso nem ingestão de água
    "3": f"Passos em '{today.isoformat()}'",
    "4": f"Passos desde '{startdate.isoformat()}' até '{today.isoformat()}'",
    "5": f"Dados de frequência cardíaca em '{today.isoformat()}'",
    "6": f"Registo da bateria corporal desde '{startdate.isoformat()}' até '{today.isoformat()}'",
    "7": f"Dados de sono em '{today.isoformat()}'",
    "8": f"Dados de stress em '{today.isoformat()}'",
    "9": f"Dados da frequência respiratória em '{today.isoformat()}'",
    "0": f"Dados de SpO2 em '{today.isoformat()}'",
    "Z": "Terminar sessão no portal do Garmin Connect",
    "q": "Sair",
}

def display_json(api_call, output):
    print(json.dumps(output, indent=4))

def create_json(output):
    return(json.dumps(output, indent=4))

def get_credentials():
    email = input("Login e-mail: ")
    password = pwinput.pwinput(prompt='Password: ')

    return email, password


def init_api(email, password):

    try:
        ## Try to load the previous session
        with open("session.json") as f:
            saved_session = json.load(f)

            print(
                "A iniciar sessão no Garmin Connect com a sessão em cache no 'session.json'...\n"
            )

            # Use the loaded session for initializing the API (without need for credentials)
            api = Garmin(session_data=saved_session)

            # Login using the
            api.login()

    except (FileNotFoundError, GarminConnectAuthenticationError):
        # Inicir sessão no Garmin Connect com novas credenciais.
        print(
            "Ficheiro de sessão inexistente ou inválido, inicie sessão com as suas credenciais do Garmin Connect.\n"
        )
        try:
            # Pedir credenciais se não estiverem definidas
            if not email or not password:
                email, password = get_credentials()

            api = Garmin(email, password)
            api.login()

            # Gravar informação de inicio de sessão em sesseio.json
            with open("session.json", "w", encoding="utf-8") as f:
                json.dump(api.session_data, f, ensure_ascii=False, indent=4)
        except (
            GarminConnectConnectionError,
            GarminConnectAuthenticationError,
            GarminConnectTooManyRequestsError
        ) as err:
            logger.error("Erro ao comunicar com o Garmin Connect: %s", err)
            return None

    return api


def print_menu():
    """menu"""
    for key in menu_options.keys():
        print(f"{key} -- {menu_options[key]}")
    print("Faça a sua seleção: ", end="", flush=True)


def switch(api, i):

    # Exit example program
    if i == "q":
        print("Obrigado!")
        sys.exit()

    # Skip requests if login failed
    if api:
        try:
            print(f"\n\nA executar: {menu_options[i]}\n")

            # USER STATISTIC SUMMARIES
            if i == "1":
                # Get activity data for 'YYYY-MM-DD'
                f = open(f'test_activity_today{today.isoformat()}.json', 'w')
                f.write(create_json(api.get_stats(today.isoformat())))
                f.close()

                # Elimina valores nulos do json
                filename = f'test_activity_today{today.isoformat()}.json'
                temp_filename = f'{filename}.tmp'
                with open(temp_filename, 'w') as temp_f:
                    with open(filename, 'r') as f:
                        dic = json.load(f)
                    new_dic = {key: value for key, value in dic.items() if value is not None}
                    json.dump(new_dic, temp_f, indent=4)
                os.replace(temp_filename, filename)


            elif i == "2":
                # Get stats and body composition data for 'YYYY-MM-DD'
                f = open(f'test_stats{today.isoformat()}.json', 'w')
                f.write(create_json(api.get_stats_and_body(today.isoformat())))
                f.close()

                # Elimina valores nulos do json
                filename = f'test_activity_today{today.isoformat()}.json'
                temp_filename = f'{filename}.tmp'
                with open(temp_filename, 'w') as temp_f:
                    with open(filename, 'r') as f:
                        dic = json.load(f)
                    new_dic = {key: value for key, value in dic.items() if value is not None}
                    json.dump(new_dic, temp_f, indent=4)
                os.replace(temp_filename, filename)
            


            # USER STATISTICS LOGGED
            elif i == "3":
                # Get steps data for 'YYYY-MM-DD'
                f = open(f'data/Steps/{today.isoformat()}.json', 'w')
                f.write(create_json(api.get_steps_data(today.isoformat())))
                f.close()
                steps_reader(f'{today.isoformat()}')
                feedback_day_steps(today)

            elif i == "4":
                # Get daily step data for 'YYYY-MM-DD'
                f = open(f'data/Week_Steps/{today.isoformat()}.json', 'w')
                f.write(create_json(api.get_daily_steps(startdate.isoformat(), today.isoformat())))
                f.close()
                week_steps_reader(f'{today.isoformat()}')

            elif i == "5":
                # Get heart rate data for 'YYYY-MM-DD'
                f = open(f'data/Heart_rate/{today.isoformat()}.json', 'w')
                f.write(create_json(api.get_heart_rates(today.isoformat())))
                f.close()
                mHr = hr_reader(f'{today.isoformat()}')
                sendToAIO('garmin-data.heart-rate', mHr)
                feedback_hr(today, mHr)
            
            elif i == "6":
                # Get daily body battery data for 'YYYY-MM-DD' to 'YYYY-MM-DD'
                f = open(f'data/Body_Battery/{today.isoformat()}.json', 'w')
                f.write(create_json(api.get_body_battery(startdate.isoformat(), today.isoformat())))
                f.close()
                body_battery_reader(f'{today.isoformat()}')
                feedback_bodybattery(today)
            
            elif i == "7":
                # Get sleep data for 'YYYY-MM-DD'
                f = open(f'data/Sleep/{today.isoformat()}.json', 'w')
                f.write(create_json(api.get_sleep_data(today.isoformat())))
                f.close()
                sleep_reader(f'{today.isoformat()}')
                duration = feedback_sleep(today)
                sendToAIO('garmin-data.sleep', duration)

            elif i == "8":
                # Get stress data for 'YYYY-MM-DD'
                f = open(f'data/Stress/{today.isoformat()}.json', 'w')
                f.write(create_json(api.get_stress_data(today.isoformat())))
                f.close()
                stress_reader(f'{today.isoformat()}')
            
            elif i == "9":
                # Get respiration data for 'YYYY-MM-DD'
                f = open(f'data/Respiration/{today.isoformat()}.json', 'w')
                f.write(create_json(api.get_respiration_data(today.isoformat())))
                f.close()
                resp_reader(f'{today.isoformat()}')

            elif i == "0":
                # Get SpO2 data for 'YYYY-MM-DD'
                f = open(f'data/SpO2/{today.isoformat()}.json', 'w')
                f.write(create_json(api.get_spo2_data(today.isoformat())))
                f.close()
                spo2_reader(f'{today.isoformat()}')

            elif i == "Z":
                # Logout Garmin Connect portal
                display_json("api.logout()", api.logout())
                api = None

        except (
            GarminConnectConnectionError,
            GarminConnectAuthenticationError,
            GarminConnectTooManyRequestsError,
            requests.exceptions.HTTPError,
        ) as err:
            logger.error("Erro: %s", err)
        except KeyError:
            # Invalid menu option chosen
            pass
    else:
        print("Não foi possível iniciar sessão no Garmin Connect.")

# Main program loop
while True:
    # Display header and login
    print("\n*** Garmin Connect API para recolha de dados ***\n")

    # Init API
    if not api:
        api = init_api(email, password)

    # Display menu
    print_menu()
    option = readchar.readkey()
    switch(api, option)