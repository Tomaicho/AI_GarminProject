import matplotlib.pyplot as plt
import json
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from statistics import mean
import pytz

local_tz = pytz.timezone('Europe/London')

def hr_reader(date):
    file = f'data\Heart_rate\{date}.json'
    dictionary = json.load(open(file, 'r'))
    timestamps = []
    heartrates = []
    high = False
    high_periodes = []
    for value in dictionary['heartRateValues']:
        if value[1] is not None:
            timestamps.append(value[0])
            heartrates.append(value[1])
            if value[1] >= 100 and high == False:
                high = True
                start_time = datetime.fromtimestamp(value[0]/1000, tz=local_tz).strftime("%H:%M")
            elif value[1] < 100 and high == True:
                high = False
                end_time = datetime.fromtimestamp(value[0]/1000, tz=local_tz).strftime("%H:%M")
                high_periodes.append((start_time, end_time))


    # Convert the timestamps to datetime objects
    timestamps = [datetime.strptime(datetime.fromtimestamp(ts/1000, tz=local_tz).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S') for ts in timestamps]

    plt.figure(figsize=(12, 6))
    plt.grid(True)

    ## LINE GRAPH ##
    plt.title(f'Frequência cardíaca - dia {date}')
    plt.plot(timestamps, heartrates, color='maroon', marker='o')
    plt.xlabel('Hora')
    plt.ylabel('FC')

    plt.show()

    print("A sua frequência cardíaca esteve bastante alta nos seguintes períodos:")
    for periodo in high_periodes:
        print(periodo[0] + ' - ' + periodo[1])
    print('''Se estes períodos não corresponderam a momentos de atividade física, o ritmo cardíaco acelerado pode dever-se a momentos de stress. Tente determinar o que poderá ter causado este stress adicional e tome ações de forma a evitá-lo. Caso não encontre nenhuma explicação plausível e isto fôr um fenómeno recorrente, consulte o seu médico, pois podem tratar-se de eventos de arritmia. Note que após uma atividade física intensiva, o ritmo cardíaco pode demorar algum tempo até estabilizar de novo no seu ritmo habitual.\n''')

    return mean(heartrates)

def steps_reader(date):
    file = f'data\Steps\{date}.json'
    dictionary = json.load(open(file, 'r'))
    timestamps = []
    steps = []
    activity = []
    for entry in dictionary:
        timestamps.append(entry['endGMT'])
        steps.append(entry['steps'])
        activity.append(entry['primaryActivityLevel'])

    # Convert the timestamps to datetime objects
    timestamps = [datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S.%f')+timedelta(hours=1) for ts in timestamps]

    plt.figure(figsize=(12, 6))
    plt.grid(True)

    ## LINE GRAPH ##
    plt.title(f'Passos {date}')
    plt.plot(timestamps, steps, color='maroon', marker='o')
    plt.xlabel('hora')
    plt.ylabel('passos')

    plt.show()


def resp_reader(date):
    file = f'data\Respiration\{date}.json'
    dictionary = json.load(open(file, 'r'))
    timestamps = []
    respiration = []
    for value in dictionary['respirationValuesArray']:
        timestamps.append(value[0])
        respiration.append(value[1])

    # Convert the timestamps to datetime objects
    timestamps = [datetime.strptime(datetime.fromtimestamp(ts/1000, tz=local_tz).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S') for ts in timestamps]

    plt.figure(figsize=(12, 6))
    plt.grid(True)

    ## LINE GRAPH ##
    plt.title(f'Frequência respiratória - dia {date}')
    plt.plot(timestamps, respiration, color='maroon', marker='o')
    plt.xlabel('hora')
    plt.ylabel('Respiração/min')

    plt.show()


def spo2_reader(date):
    file = f'data\SpO2\{date}.json'
    dictionary = json.load(open(file, 'r'))
    timestamps = []
    spo2 = []
    for value in dictionary['spO2HourlyAverages']:
        timestamps.append(value[0])
        spo2.append(value[1])

    # Convert the timestamps to datetime objects
    timestamps = [datetime.strptime(datetime.fromtimestamp(ts/1000, tz=local_tz).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S') for ts in timestamps]

    plt.figure(figsize=(12, 6))
    plt.grid(True)

    ## LINE GRAPH ##
    plt.title(f'Saturação de O2 - dia {date}')
    plt.plot(timestamps, spo2, color='maroon', marker='o')
    plt.xlabel('hora')
    plt.ylabel('SpO2')

    plt.show()


def sleep_reader(date):
    file = f'data\Sleep\{date}.json'
    dictionary = json.load(open(file, 'r'))
    timestamps_mov = []
    timestamps_stress = []
    move_score = []
    stress = []
    for value in dictionary['sleepMovement']:
        timestamps_mov.append(value['endGMT'])
        move_score.append(value['activityLevel'])

    # Convert the timestamps_mov to datetime objects
    timestamps_mov = [datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S.%f')+timedelta(hours=1) for ts in timestamps_mov]

    # Para medir o stress
    # for value in dictionary['sleepStress']:
    #     timestamps_stress.append(value['startGMT'])
    #     stress.append(value['value'])

    # Para medir a respiration
    for value in dictionary['wellnessEpochRespirationDataDTOList']:
        timestamps_stress.append(value['startTimeGMT'])
        stress.append(value['respirationValue'])

    # Convert the timestamps_stress to datetime objects
    timestamps_stress = [datetime.strptime(datetime.fromtimestamp(ts/1000, tz=local_tz).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S') for ts in timestamps_stress]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_title(f'Movimento e respiração noturnas - dia {date}')
    ax.plot(timestamps_mov, move_score, color="red")
    ax.set_xlabel("hora")
    ax.set_ylabel("Score de movimento", color="red")

    ax2=ax.twinx()
    ax2.plot(timestamps_stress, stress, color="blue")
    ax2.set_ylabel("Respiração/min",color="blue")

    plt.show()


def week_steps_reader(date):
    file = f'data\Week_Steps\{date}.json'
    dictionary = json.load(open(file, 'r'))
    dates = []
    steps = []
    goal = []
    distance = []
    for entry in dictionary:
        dates.append(entry['calendarDate'])
        steps.append(entry['totalSteps'])
        goal.append(entry['stepGoal'])
        distance.append(entry['totalDistance'])

    # Convert the timestamps to datetime objects
    dates = [datetime.strptime(ts, '%Y-%m-%d') for ts in dates]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_title(f'Passos, objetivo de passos e distância percorrida do dia {date}')
    ax.plot(dates, steps, color="red", label ='Nº de passos')
    ax.plot(dates, goal, color="gray", label ='Objetivo de passos')
    ax.set_xlabel("data")
    ax.set_ylabel("Nº passos", color="red")

    ax2=ax.twinx()
    ax2.plot(dates, distance, color="blue")
    ax2.set_ylabel("Distância (m)",color="blue", label ='Distância de passos')

    plt.show()


def body_battery_reader(date):
    file = f'data\Body_Battery\{date}.json'
    dictionary = json.load(open(file, 'r'))
    dates = []
    charged = []
    drained = []
    timestamps = []
    battery = []
    for entry in dictionary:
        dates.append(entry['date'])
        charged.append(entry['charged'])
        drained.append(entry['drained'])

    # Convert the dates to datetime Sobjects
    dates = [datetime.strptime(ts, '%Y-%m-%d') for ts in dates]
    
    # Get the values for the line graph
    for entry in dictionary:
        for instance in entry['bodyBatteryValuesArray']:
            timestamps.append(instance[0])
            battery.append(instance[1])

    # Convert the timestamps_stress to datetime objects
    timestamps = [datetime.strptime(datetime.fromtimestamp(ts/1000, tz=local_tz).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S') for ts in timestamps]

    fig, ax = plt.subplots(2, 1, figsize=(12, 6))
    barWidth = 0.25
    
    br1 = np.arange(len(dates))
    br2 = [x + 0.20 for x in br1]

    ax[0].bar(br1, charged, color ='g', width = barWidth, edgecolor ='grey', label ='carregado')
    ax[0].bar(br2, drained, color ='r', width = barWidth, edgecolor ='grey', label ='gasto')
    
    ax[0].set_xlabel('Data', fontweight ='bold', fontsize = 10)
    ax[0].set_ylabel('Bateria corporal (%)', fontweight ='bold', fontsize = 10)
    ax[0].set_xticks([r + barWidth for r in range(len(dates))], dates)
    ax[0].set_xticklabels([date.strftime("%Y-%m-%d") for date in dates])
    ax[0].set_title("Totais diários de bateria corporal carregada e gasta")
    ax[0].legend()

    ax[1].plot(timestamps,battery , color="blue")
    ax[1].set_xlabel('Data e hora', fontweight ='bold', fontsize = 10)
    ax[1].set_ylabel('Bateria corporal (%)', fontweight ='bold', fontsize = 10)
    ax[1].set_title("Evolução temporal da bateria corporal")
    ax[1].grid()

    fig.subplots_adjust(hspace=0.6)
    plt.show()


def stress_reader(date):
    file = f'data\Stress\{date}.json'
    dictionary = json.load(open(file, 'r'))
    timestamps = []
    values = []
    for value in dictionary['stressValuesArray']:
        timestamps.append(value[0])
        values.append(value[1])

    # Convert the timestamps to datetime objects
    timestamps = [datetime.strptime(datetime.fromtimestamp(ts/1000, tz=local_tz).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S') for ts in timestamps]

    plt.figure(figsize=(12, 6))
    plt.grid(True)

    ## LINE GRAPH ##
    plt.title(f'Níveis de stress - dia {date}')
    plt.plot(timestamps, values, color='maroon', marker='o')
    plt.xlabel('Hora')
    plt.ylabel('Valor de stress')

    plt.show()