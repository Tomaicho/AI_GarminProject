import matplotlib.pyplot as plt
import json
from datetime import datetime

def hr_reader(date):
    file = f'data\Heart_rate\{date}.json'
    print(file)
    dictionary = json.load(open(file, 'r'))
    timestamps = []
    heartrates = []
    for value in dictionary['heartRateValues']:
        timestamps.append(value[0])
        heartrates.append(value[1])

    # Convert the timestamps to datetime objects
    # timestamps = [datetime.fromtimestamp(ts/1000) for ts in timestamps]
    timestamps = [datetime.strptime(datetime.utcfromtimestamp(ts/1000).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S') for ts in timestamps]

    plt.grid(True)

    ## LINE GRAPH ##
    plt.title(f'Heart rate {date}')
    plt.plot(timestamps, heartrates, color='maroon', marker='o')
    plt.xlabel('timestamp')
    plt.ylabel('FC')

    plt.show()

def steps_reader(date):
    file = f'data\Steps\{date}.json'
    print(file)
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
    print(file)
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