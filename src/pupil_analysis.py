""" Functions aiming at analysing pupil's diameter in correlation to event stimuli """

from src.helpers import *
import numpy as np
import matplotlib.pyplot as plt


def get_limits(data, column):
    events = []

    # Keeping two pointers
    p1 = 0  # Pointer at the beginning of sequence
    p2 = 0  # Pointer at the end of sequence

    while p2 < len(data):
        while data[p1][column] == data[p2][column]:
            p2 += 1

            if p2 >= len(data):
                break

        events.append([data[p1][column], p1, p2-1])

        p1 = p2

    return events


def pupil_analysis(d, user, recording):

    # Creating the graph
    f, axarr = plt.subplots(3, sharex=True)

    # Getting the diameter values
    d_user = [line for line in d if line[participant] == user and line[recording_name] == recording]

    if len(d_user) is 0:
        print("No data for " + str(recording) + " for " + str(participant))
        return

    diam = [[x[time_column], x[pupil_diam_left].replace(',', '.'), x[pupil_diam_right].replace(',', '.')]
            for x in d_user[1:]]
    events = [x[time_column] for x in d_user if x[event_column] == "Logged live Event"]

    # 0: Getting the recording time values and pupil diameter
    diam_x = [float(x[0]) for x in diam if is_number(x[1]) and is_number(x[2])]
    diam_y = [(float(x[1]) + float(x[2]))/float(2) for x in diam if is_number(x[1]) and is_number(x[2])]

    # 0: Printing the values of pupil diameter
    axarr[0].set_title('Pupil diameter over time')
    axarr[0].plot(diam_x, diam_y, color='blue')

    # 0: Printing the mean value of pupil
    mean = np.array(diam_y).mean()
    axarr[0].plot((min(diam_x), max(diam_x)), (mean, mean), color='red')

    # 0: Printing the events on the map
    for event in events:
        axarr[0].plot(event, mean, marker='o', color='green')

    # 1: Pupil gradient over time
    axarr[1].set_title('Pupil gradient over time')
    grad_diam_y = np.gradient(np.array(diam_y))
    axarr[1].plot(diam_x, grad_diam_y, color='grey')
    for event in events:
        axarr[1].plot(event, min(grad_diam_y), marker='o', color='green')

    # TODO dynamically compute threshold
    threshold = 0.15
    pics_x = []
    for index in range(0, len(grad_diam_y)-1):
        if grad_diam_y[index] > threshold or grad_diam_y[index] < -threshold:
            pics_x.append(diam_x[index])

    axarr[2].set_title("Gradient optimum and events distribution")
    for event in events:
        axarr[2].plot(event, 0, marker='o', color='green')
    # TODO add lines for event positions
    for pic in pics_x:
        axarr[2].plot(pic, 1, marker='x', color='red')
    axarr[2].plot(0, -2)
    axarr[2].plot(0, 3)

    # IDEA: check if the gradient optimum arrives between the start end end of events
    """
    If they do, it means it has reaction to stimuli otherwise means he is distracted and
    cannot be used. Compute percentage of gradient pics among event times.
    """

    # Printing
    f.tight_layout()
    plt.ylabel('Pupil diameter (mm)')
    plt.xlabel('Time (ms)')
    plt.show()

