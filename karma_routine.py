import csv


def load_action_types(filename):
    result = {}
    with open(filename, newline="") as action_file:
        action_csv_reader = csv.reader(action_file, delimiter=";")
        next(action_csv_reader)
        result = {action[1]: action[0] for action in action_csv_reader}
    return result
