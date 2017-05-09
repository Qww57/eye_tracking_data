import os
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Columns index
participant = 2
recording_name = 3
time_column = 8
gaze_x_column = 9
gaze_y_column = 10
pupil_diam_left = 32
pupil_diam_right = 33
mt_column = 34               # movement type column
md_column = 35               # movement duration column
mi_column = 36               # movement index column
event_column = 39            # Event type
recording_column = 40

# Used to speed up the reading of the file by Pandas
eye_tracking_type = {
    'Project name': str,
    # 'Export date': str,
    'Recording name': str,
    'Participant name': int,
    # 'Recording start time': str
    'Recording duration': str,
    'Recording fixation filter name': str,
    'Recording timestamp': int,
    }


def is_number(str):
    try:
        float(str)
        return True
    except:
        return False


def load_all(files):
    d = []
    for file in files:
        d.extend(load(file)[1:])
    return d


def load(name):
    # Getting path to the data sample
    base = os.path.dirname(os.path.abspath(__file__))
    location = base + name

    # Converting the file to array
    unfiltered_data = []

    # Parsing the file line by line and replacing errors if encountered.
    with open(location, errors='replace') as f:
        # Basic approach to read a file
        # csv_file = pd.read_csv(f, delimiter=';', quotechar='|', dtype=eye_tracking_type)
        csv_file = csv.reader(f, delimiter=';', quotechar='|')
        for line in csv_file:
            unfiltered_data.append(line)

    # Filtering the data where Eye Tracking is not working
    return [line for line in unfiltered_data if not line[mt_column] == "EyesNotFound"]


def get_users(data):
    """
    Returns list of users contained in the array of data.
    :param data: eye tracking data as array
    :return: ordered set of users
    """
    users = list(set([line[participant] for line in data[1:]]))
    users.sort()
    return users
