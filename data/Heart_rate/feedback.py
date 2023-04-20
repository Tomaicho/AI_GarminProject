import datetime
import json
import os
import glob
import pprint
from statistics import mean, stdev
import requests

today = datetime.date.today()

def feedback_hr(date, mHr):
    files = glob.glob( 'C:/Users/tomas/Desktop/Mestrado/1A_2S/Ambientes Inteligentes/Trabalho_1/AI_GarminProject/data/Heart_rate/*.json') #only process .JSON files in folder.
    restHrsList = []
    for filename in  files[-31:]:   
        with open(filename, encoding='utf-8', mode='r') as currentFile:
            data=currentFile.read().replace('\n', '')
            rHr = json.loads(data)["restingHeartRate"]
            restHrsList.append(rHr)
    media = mean(restHrsList)
    dp = stdev(restHrsList)

    hoje = f'C:/Users/tomas/Desktop/Mestrado/1A_2S/Ambientes Inteligentes/Trabalho_1/AI_GarminProject/data/Heart_rate/{date.isoformat()}.json'
    with open(hoje, encoding='utf-8', mode='r') as currentFile:
            data=currentFile.read().replace('\n', '')
            rHr = json.loads(data)["restingHeartRate"]
    if rHr > media+dp:
        print("Esta noite, a sua frequência cardíaca em repouso foi anormalmente alta em relação aos últimos 30 dias. Isto pode dever-se a um sono agitado ou pouco profundo. Procure alterar os fatores que tenham afetado negativamente o seu sono, como a visualização excessiva de ecrãs na hora e meia precedente à sua hora de deitar.")
    elif rHr < media-dp:
        print("Esta noite, a sua frequência cardíaca em repouso foi anormalmente baixa em relação aos últimos 30 dias. Isto pode dever-se a um evento de bradicardia noturna. Consulte o seu médico se este evento se repetir mais do que três vezes.")
    else:
         print("A sua frequência cardíaca em repouso esteve dentro dos parâmetros normais esta noite.")

    # Só podemos ver cruzar dados com o weather para hoje porque não temos acesso ao histórico. Ponto a melhorar
    if date == today:
        #https://openweathermap.org/current
        api_key = "c5edae66c459cb80a6c09d9aacea3e2c"

        #url
        base_url = "http://api.openweathermap.org/data/2.5/weather?"

        #para vir em graus celsius
        graus = "&units=metric"

        #define the city
        city_name = input(f"Onde está hoje? ")

        #formar o url do pedido
        full_url = base_url + "appid=" + api_key + "&q=" + city_name + graus
        response = requests.get(full_url)
        x = response.json()

        if x["cod"] != "404":
            y = x["main"]
            if mHr > 72:
                if y["humidity"] > 95 and y["temp"] > 30:
                    print(f'Hoje a sua frequência cardíaca foi bastante superior à média dos últimos 30 dias. Contudo, isto pode ter-se devido aos elevados valores de humidade {y["humidity"]} e temperatura {y["temp"]} sentidos.')
                elif y["humidity"] > 95 and y["temp"] < 30:
                    print(f'Hoje a sua frequência cardíaca foi bastante superior à média dos últimos 30 dias. Contudo, isto pode ter-se devido aos elevados valores de humidade {y["humidity"]} sentidos.')
                elif y["humidity"] < 95 and y["temp"] > 30:
                    print(f'Hoje a sua frequência cardíaca foi bastante superior à média dos últimos 30 dias. Contudo, isto pode ter-se devido aos elevados valores de temperatura {y["temp"]} sentidos.')
                else:
                    print('Hoje a sua frequência cardíaca foi bastante superior à média dos últimos 30 dias.')
