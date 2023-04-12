import matplotlib.pyplot as plt
import json
from datetime import datetime
import numpy as np
import pandas as pd

def hr_reader(date):
    file = f'data\Heart_rate\{date}.json'
    dictionary = json.load(open(file, 'r'))
    timestamps = []
    heartrates = []
    for value in dictionary['heartRateValues']:
        timestamps.append(value[0])
        heartrates.append(value[1])

    # Convert the timestamps to datetime objects
    timestamps = [datetime.strptime(datetime.utcfromtimestamp(ts/1000).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S') for ts in timestamps]

    plt.figure(figsize=(12, 6))
    plt.grid(True)

    ## LINE GRAPH ##
    plt.title(f'Heart rate {date}')
    plt.plot(timestamps, heartrates, color='maroon', marker='o')
    plt.xlabel('timestamp')
    plt.ylabel('FC')

    plt.show()

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
    timestamps = [datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S.%f') for ts in timestamps]

    plt.figure(figsize=(12, 6))
    plt.grid(True)

    ## LINE GRAPH ##
    plt.title(f'Passos {date}')
    plt.plot(timestamps, steps, color='maroon', marker='o')
    plt.xlabel('timestamp')
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
    timestamps = [datetime.strptime(datetime.utcfromtimestamp(ts/1000).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S') for ts in timestamps]

    plt.figure(figsize=(12, 6))
    plt.grid(True)

    ## LINE GRAPH ##
    plt.title(f'Respiration frequency {date}')
    plt.plot(timestamps, respiration, color='maroon', marker='o')
    plt.xlabel('timestamp')
    plt.ylabel('Respiration')

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
    timestamps = [datetime.strptime(datetime.utcfromtimestamp(ts/1000).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S') for ts in timestamps]

    plt.figure(figsize=(12, 6))
    plt.grid(True)

    ## LINE GRAPH ##
    plt.title(f'Spo2 {date}')
    plt.plot(timestamps, spo2, color='maroon', marker='o')
    plt.xlabel('timestamp')
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
    timestamps_mov = [datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S.%f') for ts in timestamps_mov]

    for value in dictionary['sleepStress']:
        timestamps_stress.append(value['startGMT'])
        stress.append(value['value'])

    # Convert the timestamps_stress to datetime objects
    timestamps_stress = [datetime.strptime(datetime.utcfromtimestamp(ts/1000).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S') for ts in timestamps_stress]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_title('Sleep Movement and Stress')
    ax.plot(timestamps_mov, move_score, color="red")
    ax.set_xlabel("timestamp")
    ax.set_ylabel("Movement Score", color="red")

    ax2=ax.twinx()
    ax2.plot(timestamps_stress, stress, color="blue")
    ax2.set_ylabel("Stress Score",color="blue")

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
    ax.set_title('Daily steps, steps goal and steps distance')
    ax.plot(dates, steps, color="red")
    ax.plot(dates, goal, color="gray")
    ax.set_xlabel("date")
    ax.set_ylabel("Steps", color="red")

    ax2=ax.twinx()
    ax2.plot(dates, distance, color="blue")
    ax2.set_ylabel("Steps distance (m)",color="blue")

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
    timestamps = [datetime.strptime(datetime.utcfromtimestamp(ts/1000).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S') for ts in timestamps]

    fig, ax = plt.subplots(2, 1, figsize=(12, 6))
    barWidth = 0.25
    
    br1 = np.arange(len(dates))
    br2 = [x + 0.20 for x in br1]

    ax[0].bar(br1, charged, color ='g', width = barWidth, edgecolor ='grey', label ='charged')
    ax[0].bar(br2, drained, color ='r', width = barWidth, edgecolor ='grey', label ='drained')
    
    ax[0].set_xlabel('Date', fontweight ='bold', fontsize = 10)
    ax[0].set_ylabel('Body Battery (%)', fontweight ='bold', fontsize = 10)
    ax[0].set_xticks([r + barWidth for r in range(len(dates))], dates)
    ax[0].set_xticklabels([date.strftime("%Y-%m-%d") for date in dates])
    ax[0].set_title("Daily Body Battery total drainage and charging")
    ax[0].legend()

    ax[1].plot(timestamps,battery , color="blue")
    ax[1].set_xlabel('Timestamp', fontweight ='bold', fontsize = 10)
    ax[1].set_ylabel('Body Battery (%)', fontweight ='bold', fontsize = 10)
    ax[1].set_title("Body Battery evolution")
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
    timestamps = [datetime.strptime(datetime.utcfromtimestamp(ts/1000).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S') for ts in timestamps]

    plt.figure(figsize=(12, 6))
    plt.grid(True)

    ## LINE GRAPH ##
    plt.title(f'Stress Levels {date}')
    plt.plot(timestamps, values, color='maroon', marker='o')
    plt.xlabel('timestamp')
    plt.ylabel('Stress Value')

    plt.show()