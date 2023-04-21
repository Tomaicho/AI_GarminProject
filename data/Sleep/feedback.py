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
                 if activity < 2.0: #Definiu-se 2.0 como o threshold, pois todos os valores comprovadamente a dormir eram inferiores a 2.6
                    movLevelList.append(activity)
        media_dia = mean(movLevelList)
        medias_diarias.append(media_dia)
    
    media = mean(medias_diarias)
    dp = stdev(medias_diarias)

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
                elif activity > 3.0:
                    if sleep == True:
                        sleep = False
                        end_time = datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S.%f')
                        sleep_periodes.append((start_time, end_time))
                        sleep_duration += end_time - start_time
            media_hoje = mean(movLevelList)
    if media_hoje > media+dp:
        print("A sua atividade noturna esta noite esteve acima do padrão normal dos últimos 30 dias.\n")
    elif media_hoje < media-dp:
        print("A sua atividade noturna esta noite foi mais baixa do que o padrão dos últimos 30 dias.\n")
    else:
         print("A sua atividade noturna esta noite esteve dentro dos parâmetros normais.\n")
    
    print(f'A duração do seu sono no dia {date.isoformat()} foi de: ', sleep_duration,'\n')
    sleep_duration = int(sleep_duration.total_seconds()/60)
    if sleep_duration >= 480:
        print("Dormiu mais do que o número mínimo de horas de sono recomendado. Bom desempenho!\n")
    elif sleep_duration < 480 and sleep_duration > 420:
        print("Dormiu um pouco menos do que o número mínimo de horas de sono recomendado que é de 8h. Procure aumentar ligeiramente o seu tempo de sono para evitar complicações de saúde no futuro.\n")
    else:
        print('O seu número de horas de sono hoje foi insuficiente. Evite este comportamento de uma forma repetitiva. Se dedica o tempo necessário mas não consegue adormecer, consulte o seu médico.\n')

    return sleep_duration