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
    processed_profiles = profiles[:]
    for profile in processed_profiles:
        profile["karma"] = sum([actions[action] for action in profile["actions"]])

    return processed_profiles


def write_solution(filename, actions, profiles):
    profiles_with_karma = calculate_karma(actions, profiles)

    with open(filename, "w", newline="") as output_file:
        writer = csv.DictWriter(output_file, profiles_with_karma.keys(), delimiter=";")
        writer.writeheader()
        writer.writerows(profiles_with_karma)


if __name__ == "__main__":
    write_solution("challenge-1.csv",
                   load_action_types("karma.csv"),
                   load_person_profiles("profiles.csv"))
