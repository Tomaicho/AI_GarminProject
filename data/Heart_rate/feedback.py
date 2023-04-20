import json
import os
import glob
import pprint
from statistics import mean, stdev

def feedback_hr():
    files = glob.glob( 'C:/Users/tomas/Desktop/Mestrado/1A_2S/Ambientes Inteligentes/Trabalho_1/AI_GarminProject/data/Heart_rate/*.json') #only process .JSON files in folder.
    restHrsList = []
    for filename in  files[-31:]:   
        with open(filename, encoding='utf-8', mode='r') as currentFile:
            data=currentFile.read().replace('\n', '')
            rHr = json.loads(data)["restingHeartRate"]
            restHrsList.append(rHr)
    media = mean(restHrsList)
    dp = stdev(restHrsList)

    today = files[-1]
    with open(today, encoding='utf-8', mode='r') as currentFile:
            data=currentFile.read().replace('\n', '')
            rHr = json.loads(data)["restingHeartRate"]
    if rHr > media+dp:
        print("Esta noite, a sua frequência cardíaca em repouso foi anormalmente alta em relação aos últimos 30 dias. Isto pode dever-se a um sono agitado ou pouco profundo. Procure alterar os fatores que tenham afetado negativamente o seu sono, como a visualização excessiva de ecrãs na hora e meia precedente à sua hora de deitar.")
    elif rHr < media-dp:
        print("Esta noite, a sua frequência cardíaca em repouso foi anormalmente baixa em relação aos últimos 30 dias. Isto pode dever-se a um evento de bradicardia noturna. Consulte o seu médico se este evento se repetir mais do que três vezes.")
    else:
         print("A sua frequência cardíaca em repouso esteve dentro dos parâmetros normais esta noite.")