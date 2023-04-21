import json
from statistics import mean, stdev

def feedback_bodybattery(date):
    offsets = []
    bad_days = []
    drained_list = []
    charged_list = []
    negative = False
    file = f'C:/Users/tomas/Desktop/Mestrado/1A_2S/Ambientes Inteligentes/Trabalho_1/AI_GarminProject/data/Body_Battery/{date}.json'
    with open(file, encoding='utf-8', mode='r') as currentFile:
        data=currentFile.read().replace('\n', '')
        days = json.loads(data)
        for day in days:
            charged = day["charged"]
            drained = day["drained"]
            drained_list.append(drained)
            charged_list.append(charged)
            offset = charged - drained
            offsets.append(offset)
            if offset < 0:
                negative = True
                bad_days.append((day["date"], offset))
    
    week_offset = sum(offsets)
    mean_drained = mean(drained_list)
    mean_charged = mean(charged_list)

    if -20 < week_offset < 0:
        print(f"Ao longo desta semana, o seu gasto de energia foi ligeiramente superior ao que recuperou durante o sono. No total, gastou mais {-week_offset}% de energia do que a que recuperou. Pode reverter esta situação aumentando o seu tempo de sono diário ou a qualidade deste. Algumas estratégias passam por melhorar as condições do seu local de pernoita, como escurecê-lo melhor ou arranjar uma forma de o manter arejado.\n")
    elif week_offset <= -20:
         print(f"Ao longo desta semana, o seu gasto de energia foi superior ao que recuperou durante o sono. No total, gastou mais {-week_offset}% de energia do que a que recuperou. Sendo esta uma situação limite, avaliada ao longo dos últimos 7 dias, deve tentar revertê-la o mais rápido possível para evitar complicações de saúde. Pode reverter esta situação aumentando o seu tempo de sono diário ou a qualidade deste. Algumas estratégias passam por melhorar as condições do seu local de pernoita, como escurecê-lo melhor ou arranjar uma forma de o manter arejado. Caso estas estratégias não resultem deve contactar o seu médico.\n")
    else:
        print("Nos últimos 7 dias, o seu gasto total de energia foi inferior à energia recuperada durante o sono. Continue assim para se manter energético!\n")

    print(f'Nos últimos sete dias, o seu gasto diário de bateria corporal foi em média de {mean_drained}% e a recuperação foi em média de {mean_charged}.')

    if negative == True:
        print('Gastou mais energia do que a que recuperou nos seguintes dias:')
        for day in bad_days:
            print(f'{day[0]} -> {day[1]}%')