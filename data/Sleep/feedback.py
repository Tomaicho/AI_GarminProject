import json
import os
import glob
from statistics import mean, stdev
from datetime import datetime, timedelta

movLevelList = []
medias_diarias = []
def feedback_sleep(date):
    files = glob.glob( 'C:/Users/tomas/Desktop/Mestrado/1A_2S/Ambientes Inteligentes/Trabalho_1/AI_GarminProject/data/Sleep/*.json') #only process .JSON files in folder.
    for filename in  files[-31:]:   
        with open(filename, encoding='utf-8', mode='r') as currentFile:
            data=currentFile.read().replace('\n', '')
            sleepMovList = json.loads(data)["sleepMovement"]
            for mov_entry in sleepMovList:
                 activity = mov_entry["activityLevel"]
                 if activity < 2.5: #Definiu-se 2.5 como o threshold, pois todos os valores comprovadamente a dormir eram inferiores a 2.6
                    movLevelList.append(activity)
        media_dia = mean(movLevelList)
        medias_diarias.append(media_dia)
    
    media = mean(medias_diarias)
    dp = stdev(medias_diarias)
    print('Média: ', media)
    print('D-P: ', dp)

    today = f'C:/Users/tomas/Desktop/Mestrado/1A_2S/Ambientes Inteligentes/Trabalho_1/AI_GarminProject/data/Sleep/{date.isoformat()}.json'
    sleep = False
    sleep_periodes = []
    sleep_duration = timedelta(0)
    with open(today, encoding='utf-8', mode='r') as currentFile:
            data=currentFile.read().replace('\n', '')
            sleepMovList = json.loads(data)["sleepMovement"]
            for mov_entry in sleepMovList:
                activity = mov_entry["activityLevel"]
                ts = mov_entry['startGMT']
                if activity < 2.0:
                    movLevelList.append(activity)
                    if sleep == False:
                        sleep = True
                        start_time = datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S.%f')#Regista hora de início do sono
                        print('Start: ', start_time)
                elif activity > 3.0:
                    if sleep == True:
                        sleep = False
                        end_time = datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S.%f')
                        print('End: ', end_time)
                        sleep_periodes.append((start_time, end_time))
                        sleep_duration += end_time - start_time
            media_hoje = mean(movLevelList)
            print('Média hoje: ', media_hoje)
    if media_hoje > media+dp:
        print("A sua atividade noturna esta noite esteve acima dos padrão normal dos últimos 30 dias.")
    elif media_hoje < media-dp:
        print("A sua atividade noturna esta noite foi mais baixa do que o padrão dos últimos 30 dias.")
    else:
         print("A sua atividade noturna esta noite esteve dentro dos parâmetros normais.")
    
    print(f'A duração do seu sono no dia {date.isoformat()} foi de: ', sleep_duration)

    return str(sleep_duration)
    # for period in sleep_periodes:
    #     duration = 
    
    # # Adaptar isto!
    
    # for value in dictionary['heartRateValues']:
    #     if value[1] is not None:
    #         timestamps.append(value[0])
    #         heartrates.append(value[1])
    #         if value[1] >= 95 and high == False:
    #             high = True
    #             start_time = datetime.utcfromtimestamp(value[0]/1000).strftime("%H:%M")
    #         elif value[1] < 95 and high == True:
    #             high = False
    #             end_time = datetime.utcfromtimestamp(value[0]/1000).strftime("%H:%M")
    #             high_periodes.append((start_time, end_time))