#!/usr/bin/env python3
import argparse
import json
import sys


def error(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)


def parse_input(input):
    try:
        with open(input) as f:
            return json.load(f)
    except ValueError as ve:
        error(f"Unable to parse input")


class Parameters(object):

    def __init__(self, input):
        self._input = input
        self.scooters = self._input['scooters']

        if 'C' in self._input:
            self.manager_capacity = self._input['C']
        else:
            error(f"No 'C' defined in input")

        if 'P' in self._input:
            self.engineer_capacity = self._input['P']
        else:
            error(f"No 'P' defined in input")

        self.__check()

    def __check(self):
        # Check number of districts
        nb_district = self.scooters.__len__()
        self.__check_in_bound(nb_district, 1, 100, "Number of districts")

        # Check number of scooters per district
        for index, nb_scooters in enumerate(self.scooters):
            self.__check_in_bound(nb_scooters, 0, 1000, f"District {index}")

        # Check manager capacity
        self.__check_in_bound(self.manager_capacity, 1, 999, "Manager capacity")

        # Check engineer capacity
        self.__check_in_bound(self.engineer_capacity, 1, 1000, "Engineer capacity")

    def __check_in_bound(self, value, min, max, prefix):
        if not min <= value <= max:
            error(f"{prefix} out of bounds [{min}, {max}] : {value}")


class Output:
    def __init__(self, value):
        self.fleet_engineers = value

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


def main(input_file):
    input = parse_input(input_file)

    parameters = Parameters(input)

    nb_eng = 0
    for num in parameters.scooters:
        sold = num - parameters.manager_capacity
        nb_eng += 1
        while sold > 0:
            sold = sold - parameters.engineer_capacity
            nb_eng += 1

    print(Output(nb_eng).toJSON())


parser = argparse.ArgumentParser(description='Compute number of engineers to maintain scooters park.')
parser.add_argument('-f', '--file', dest='file', action='store', help='Specify the input file', required=True)

args = parser.parse_args()

main(args.file)