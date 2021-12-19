import csv
from karma_routine import load_person_profiles
import random

NAUGHTY_PRESENT = "a piece of coal"


def load_present_types(filename):
    with open(filename, newline="") as presents_file:
        present_reader = csv.reader(presents_file, delimiter=";")
        next(present_reader)
        result = {present[0]: present[1] for present in present_reader}
    return result


def get_random_present(present_types, desired_present_type):
    return random.choice(present_types[desired_present_type].split(","))


def is_naughty(person):
    return person["karma"] < 0


def is_very_good(person):
    return person["karma"] >= 7


def calc_presents(profiles, present_types):
    processed_profiles = profiles[:]
    for person in processed_profiles:
        if is_naughty(person):
            person["presents"] = [NAUGHTY_PRESENT]
        else:
            present_preferences = person["ideal present categories"].split(",")
            person["presents"] = [get_random_present(present_types, present_preferences[0])]
            if is_very_good(person):
                person["presents"].append(get_random_present(present_types, present_preferences[1]))
    return processed_profiles


def write_solution(filename, present_types, profiles):
    profiles_with_presents = calc_presents(profiles, present_types)
    with open(filename, "w", newline="") as output_file:
        writer = csv.DictWriter(output_file, [
            "name", "actions", "karma", "ideal present categories", "presents"
        ])
        writer.writeheader()
        for person in profiles_with_presents:
            person["presents"] = ",".join(person["presents"])
            writer.writerow(person)
