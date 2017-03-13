""" Main class of the project aiming at analysing Eye Tracking Data """

import time

from src.helpers import load_all, get_users
from src.pupil_analysis import pupil_analysis
from src.stats import describe_quantitative


def main():
    print("Start of the algorithm")
    debut = time.time()

    files = [
        "\\..\\data\\all_data_1.csv",
        "\\..\\data\\all_data_2.csv"
    ]

    # Loading the data
    d = load_all(files)
    print("Data loaded: " + str(len(d)) + " lines in " + str(int(time.time() - debut)) + " seconds")
    debut = time.time()

    # Getting the list of users
    users = get_users(d)
    print("List of user IDs: " + str(users))

    # Describing quantitatively the file
    describe_quantitative(d, users, save=False)
    print("Graphs created in " + str(int(time.time() - debut)) + " seconds")

    # Describe pupil diameter of one specific recording
    pupil_analysis(d, "22", "Recording089")

main()
