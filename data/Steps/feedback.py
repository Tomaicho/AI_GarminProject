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
            if steps < 300:
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
            if 300 <= steps < 1000:
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
            if steps >= 1000:
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
    
    print('Intervalos temporais agrupados por nível de atividade\n(ATENÇÃO: este nível de atividade diz apenas respeito aos passos registados pelo acelerómetro. Atividades como ciclismo não são tidas em conta por não haver movimento do braço.)')
    print('-> Sedentário:')
    for interval in sedentary_intervals:
        print(f'{interval[0]} - {interval[1]}')
    
    print('\n-> Ativo:')
    for interval in active_intervals:
        print(f'{interval[0]} - {interval[1]}')
    
    print('\n-> Muito ativo:')
    for interval in highly_active_intervals:
        print(f'{interval[0]} - {interval[1]}')

    if total_steps < 10000:
        print('Hoje, o seu nível de atividade resgistada em número de passos foi baixo. Procure reduzir o seu sedentarismo dedicando algum tempo do seu dia à prática de atividade física. O sedentarismo prolongado pode levar a diversos problemas de saúde, desde imunodepressão a complicações articulares.')
    else:
        print("O número de passos registados hoje indica que teve um dia bastante ativo. Continue assim para manter uma vida saudável!")

