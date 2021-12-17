import csv


def load_action_types(filename):
    result = {}
    with open(filename, newline="") as action_file:
        action_csv_reader = csv.reader(action_file, delimiter=";")
        next(action_csv_reader)
        result = {action[1]: 1 if action[0] == "nice" else -1 for action in action_csv_reader}
    return result


def load_person_profiles(filename):
    result = []
    with open(filename, newline="") as profile_file:
        profile_reader = csv.DictReader(profile_file, delimiter=";")
        for person in profile_reader:
            person["actions"] = person["actions"].split(",")
            person["ideal present categories"] = person["ideal present categories"].split(",")
            result.append(person)
    return result


def calculate_karma(actions, profiles):
    pass
