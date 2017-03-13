""" Functions aiming at analysing quantitatively eye tracking data of users """


from src.helpers import *


def fixation_key(user):
    return "all " + str(float(user)) + ' - Fixation time (ms)'


def saccade_key(user):
    return "all " + str(float(user)) + ' - Saccade time (ms)'


def gaze_x_key(user):
    return "all " + str(float(user)) + ' - Gaze X (pixels)'


def gaze_y_key(user):
    return "all " + str(float(user)) + ' - Gaze Y (pixels)'


keys = {'fixation': fixation_key, 'saccade': saccade_key, 'gaze_x': gaze_x_key, 'gaze_y': gaze_y_key}


def quantitative(raw_data, user_id, type):
    raw_data = raw_data[1:]

    def analyse_records(data, user_id):
        # Fixation and saccade times
        pd1 = pd.DataFrame(list(set([float(line[md_column]) for line in data if line[mt_column] == "Fixation"])),
                           columns=[str(user_id) + ' - Fixation time (ms)']).describe(include='all')
        pd2 = pd.DataFrame(list(set([float(line[md_column]) for line in data if line[mt_column] == "Saccade"])),
                           columns=[str(user_id) + ' - Saccade time (ms)']).describe(include='all')

        # X and Y coordinates of gaze points
        pd3 = pd.DataFrame([float(line[gaze_x_column]) for line in data if is_number(line[gaze_x_column])],
                           columns=[str(user_id) + ' - Gaze X (pixels)']).describe(include='all')
        pd4 = pd.DataFrame([float(line[gaze_y_column]) for line in data if is_number(line[gaze_y_column])],
                           columns=[str(user_id) + ' - Gaze Y (pixels)']).describe(include='all')

        return pd.concat([pd1, pd2, pd3, pd4], axis=1)

    if type == "all":
        data = [line for line in raw_data if float(line[participant]) == user_id]
        return analyse_records(data, "all " + str(user_id))

    if type == "each":
        records = list(set([line[recording_name] for line in raw_data if float(line[participant]) == user_id]))
        records.sort()
        dfs = pd.DataFrame()
        for rec in records:
            data = [line for line in raw_data if line[recording_name] == rec]
            dfs = pd.concat([dfs, analyse_records(data, str(user_id) + " - " + str(rec))], axis=1)
        return dfs


def describe_quantitative(d, users, save=True):
    """
    :param d:
    :param users:
    :param save:
    :return:
    """

    # Showing: fixation, saccade, gaze X, gaze Y on average
    f, axarr = plt.subplots(4, sharex=True)
    users_int = [int(user) for user in users]
    axarr[0].set_xlim([min(users_int)-1, max(users_int)+1])
    axarr[0].set_title("Average fixation time")
    axarr[0].set_ylabel("time (ms)")
    axarr[1].set_title("Average saccade time")
    axarr[1].set_ylabel("time (ms)")
    axarr[2].set_title("Average Gaze X position")
    axarr[2].set_ylim([0, 1920])
    axarr[2].set_ylabel("position (pixel)")
    axarr[3].set_title("Average Gaze Y position (not reversed)")
    axarr[3].set_ylim([0, 1080])
    axarr[3].set_ylabel("position (pixel)")

    def plot_describe(data_frame, pos):
        data_array = data_frame.as_matrix()
        for index in range(0, len(data_array[0])):
            axarr[pos].errorbar(int(users[index]), data_array[1][index], data_array[2][index], fmt='ok', lw=3)
            axarr[pos].errorbar(int(users[index]), data_array[1][index],
                         [[data_array[1][index] - data_array[3][index]], [data_array[7][index] - data_array[1][index]]],
                         fmt='.k', color='gray', lw=1)

    def plot_one_value(value, pos):
        data_frame = pd.DataFrame()
        for user in users:
            result = pd.concat([quantitative(d, float(user), "all"), quantitative(d, float(user), "each")], axis=1)

            # Saving the results into CSV
            if save is True:
                base = os.path.dirname(os.path.abspath(__file__))
                location = base + "\\results\\" + str(user) + "_results.csv"
                result.to_csv(location, sep=';')

            key = keys[value](user)
            data_frame = pd.concat([data_frame, pd.DataFrame(result, columns=[key])], axis=1)
        plot_describe(data_frame, pos)

    plot_one_value('fixation', 0)
    plot_one_value('saccade', 1)
    plot_one_value('gaze_x', 2)
    plot_one_value('gaze_y', 3)
    plt.xlabel('User ID')
    plt.show()







