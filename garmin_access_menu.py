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
print('today: ', today)
startdate = today - datetime.timedelta(days=7) # Selecionar a última semana
start = 0
limit = 100
activitytype = ""  # Valores possíveis: cycling, running, swimming, multi_sport, fitness_equipment, hiking, walking, other

menu_options = {
    "1": f"Resumo do dia em '{today.isoformat()}'",
    "2": f"Informação estatística e composição corporal em '{today.isoformat()}'", # Composição corporal inexistente porque não registo peso nem ingestão de água
    "3": f"Passos em '{today.isoformat()}'",
    "4": f"Passos desde '{startdate.isoformat()}' até '{today.isoformat()}'",
    "5": f"Dados de frequência cardíaca em '{today.isoformat()}'",
    "6": f"Registo da bateria corporal desde '{startdate.isoformat()}' até '{today.isoformat()}'",
    "7": f"Condição de treino em '{today.isoformat()}'", # Este não funciona tão bem porque não tenho corrido
    "0": f"Dados de sono em '{today.isoformat()}'",
    "a": f"Dados de stress em '{today.isoformat()}'",
    "b": f"Dados da frequência respiratória em '{today.isoformat()}'",
    "c": f"Dados de SpO2 em '{today.isoformat()}'",
    "e": f"Atividades desde início '{start}' até '{limit}'",
    "f": "Última atividade",
    "g": f"Resumo da progressão física desde '{startdate.isoformat()}' até '{today.isoformat()}' para todas as métricas",
    "Z": "Terminar sessão no portal do Garmin Connect",
    "q": "Sair",
}

def display_json(api_call, output):

    # dashed = "-"*20
    # header = f"{dashed} {api_call} {dashed}"
    # footer = "-"*len(header)

    # print(header + json.dumps(output, indent=4) + footer)
    # return(header + json.dumps(output, indent=4) + footer)
    print(json.dumps(output, indent=4))

def create_json(output):
    return(json.dumps(output, indent=4))

def display_text(output):

    dashed = "-"*60
    header = f"{dashed}"
    footer = "-"*len(header)

    print(header)
    print(json.dumps(output, indent=4))
    print(footer)

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


            # USER STATISTICS LOGGED
            elif i == "3":
                # Get steps data for 'YYYY-MM-DD'
                f = open(f'data/Steps/{today.isoformat()}.json', 'w')
                f.write(create_json(api.get_steps_data(today.isoformat())))
                f.close()
                steps_reader(f'{today.isoformat()}')

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
                feedback_hr()
            
            elif i == "6":
                # Get daily body battery data for 'YYYY-MM-DD' to 'YYYY-MM-DD'
                f = open(f'data/Body_Battery/{today.isoformat()}.json', 'w')
                f.write(create_json(api.get_body_battery(startdate.isoformat(), today.isoformat())))
                f.close()
                body_battery_reader(f'{today.isoformat()}')
                
            elif i == "7":
                # Get training status data for 'YYYY-MM-DD'
                f = open(f'test_train_status{today.isoformat()}.json', 'w')
                f.write(create_json(api.get_training_status(today.isoformat())))
                f.close()
            
            elif i == "0":
                # Get sleep data for 'YYYY-MM-DD'
                f = open(f'data/Sleep/{today.isoformat()}.json', 'w')
                f.write(create_json(api.get_sleep_data(today.isoformat())))
                f.close()
                sleep_reader(f'{today.isoformat()}')
                duration = feedback_sleep(today)
                sendToAIO('garmin-data.sleep', duration)

            elif i == "a":
                # Get stress data for 'YYYY-MM-DD'
                f = open(f'data/Stress/{today.isoformat()}.json', 'w')
                f.write(create_json(api.get_stress_data(today.isoformat())))
                f.close()
                stress_reader(f'{today.isoformat()}')
            
            elif i == "b":
                # Get respiration data for 'YYYY-MM-DD'
                f = open(f'data/Respiration/{today.isoformat()}.json', 'w')
                f.write(create_json(api.get_respiration_data(today.isoformat())))
                f.close()
                resp_reader(f'{today.isoformat()}')

            elif i == "c":
                # Get SpO2 data for 'YYYY-MM-DD'
                f = open(f'data/SpO2/{today.isoformat()}.json', 'w')
                f.write(create_json(api.get_spo2_data(today.isoformat())))
                f.close()
                spo2_reader(f'{today.isoformat()}')
            
            # ACTIVITIES
            elif i == "e":
                # Get activities data from start and limit
                f = open(f'test_activities{today.isoformat()}.json', 'w')
                f.write(create_json(api.get_activities(start, limit))) # 0=start, 1=limit
                f.close()

                filename = f'test_activities{today.isoformat()}.json'
                temp_filename = f'{filename}.tmp'
                with open(temp_filename, 'w') as temp_f:
                    with open(filename, 'r') as f:
                        new_list = []
                        list = json.load(f)
                    for dic in list:
                        new_dic = {key: value for key, value in dic.items() if value is not None}
                        new_list.append(new_dic)

                    json.dump(new_list, temp_f, indent=4)
                os.replace(temp_filename, filename)
            
            elif i == "f":
                # Get last activity
                f = open(f'test_last_activity{today.isoformat()}.json', 'w')
                f.write(create_json(api.get_last_activity()))
                f.close()

                filename = f'test_last_activity{today.isoformat()}.json'
                temp_filename = f'{filename}.tmp'
                with open(temp_filename, 'w') as temp_f:
                    with open(filename, 'r') as f:
                        dic = json.load(f)
                    new_dic = {key: value for key, value in dic.items() if value is not None}
                    json.dump(new_dic, temp_f, indent=4)
                os.replace(temp_filename, filename)

            elif i == "g":
                # Get progress summary
                f = open(f'test_progress{today.isoformat()}.json', 'w')
                for metric in ["elevationGain", "duration", "distance", "movingDuration"]:
                    f.write(create_json(
                        api.get_progress_summary_between_dates(startdate.isoformat(), today.isoformat(), metric)))
                f.close()

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