import csv
from karma_routine import load_person_profiles
import random


def load_present_types(filename):
    with open(filename, newline="") as presents_file:
        present_reader = csv.reader(presents_file, delimiter=";")
        next(present_reader)
        result = {present[0]: present[1] for present in present_reader}
    return result
