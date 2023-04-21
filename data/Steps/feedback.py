import json
from statistics import mean, stdev
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def feedback_day_steps(date):
    total_time_sedentary = 0
    total_time_active = 0
    total_time_highlyactive = 0
    total_steps = 0
    sedentary_intervals = []
    active_intervals = []
    highly_active_intervals = []
    sedentary = False
    active = False
    highly_active = False
    status_list = []
    file = f'C:/Users/tomas/Desktop/Mestrado/1A_2S/Ambientes Inteligentes/Trabalho_1/AI_GarminProject/data/Steps/{date}.json'
    with open(file, encoding='utf-8', mode='r') as currentFile:
        data=currentFile.read().replace('\n', '')
        intervals = json.loads(data)
        for interval in intervals:
            steps = interval['steps']
            total_steps += steps
            #Sedentário
            if steps < 200:
                total_time_sedentary += 15
                if sedentary == False:
                    sedentary = True
                    start_time_s = datetime.strptime(interval["startGMT"], '%Y-%m-%dT%H:%M:%S.%f') + timedelta(hours=1)
                    start_time_s = start_time_s.strftime("%H:%M")
                    status_list.append((start_time_s, 'sedentary'))
            else:
                if sedentary == True:
                    sedentary = False
                    end_time_s = datetime.strptime(interval["startGMT"], '%Y-%m-%dT%H:%M:%S.%f') + timedelta(hours=1)
                    end_time_s = end_time_s.strftime("%H:%M")
                    sedentary_intervals.append((start_time_s,end_time_s))
            
            #Ativo
            if 200 <= steps < 700:
                total_time_active += 15
                if active == False:
                    active = True
                    start_time_a = datetime.strptime(interval["startGMT"], '%Y-%m-%dT%H:%M:%S.%f') + timedelta(hours=1)
                    start_time_a = start_time_a.strftime("%H:%M")
                    status_list.append((start_time_a, 'active'))
            else:
                if active == True:
                    active = False
                    end_time_a = datetime.strptime(interval["startGMT"], '%Y-%m-%dT%H:%M:%S.%f') + timedelta(hours=1)
                    end_time_a = end_time_a.strftime("%H:%M")
                    active_intervals.append((start_time_a, end_time_a))

            #Muito ativo
            if steps >= 700:
                total_time_highlyactive += 15
                if highly_active == False:
                    highly_active = True
                    start_time_ha = datetime.strptime(interval["startGMT"], '%Y-%m-%dT%H:%M:%S.%f') + timedelta(hours=1)
                    start_time_ha = start_time_ha.strftime("%H:%M")
                    status_list.append((start_time_ha, 'highly_active'))
            else:
                if highly_active == True:
                    highly_active = False
                    end_time_ha = datetime.strptime(interval["startGMT"], '%Y-%m-%dT%H:%M:%S.%f') + timedelta(hours=1)
                    end_time_ha = end_time_ha.strftime("%H:%M")
                    highly_active_intervals.append((start_time_ha, end_time_ha))
    
    print('Intervalos :')
    for interval in sedentary_intervals:
        print(f'{interval[0]} - {interval[1]}')
    
    print('ativo:')
    for interval in active_intervals:
        print(f'{interval[0]} - {interval[1]}')
    
    print('muito-ativo:')
    for interval in highly_active_intervals:
        print(f'{interval[0]} - {interval[1]}')

    
    timestamps = [t[0] for t in status_list]
    status = [s[1] for s in status_list]

    plt.figure(figsize=(12, 6))
    plt.grid(True)

    ## LINE GRAPH ##
    plt.title(f'Nível de atividade ao longo do dia: {date}')
    plt.plot(timestamps, status, color='maroon', marker='o')
    plt.xlabel('Hora')
    plt.ylabel('Nível de atividade')

    plt.show()

