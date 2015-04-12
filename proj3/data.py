from collections import defaultdict
import csv


def ParseFile(filename):
    integrated_dataset = []
    cross_streets = defaultdict(list)
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            accident_list = set()
            # reasons
            accident_list.update(x for x in row[18:23] if x and x != 'Unspecified')
            # streets
            accident_list.update(x for x in row[7:8] if x)
            # vehicles
            accident_list.update(x for x in row[24:29] if x and x != 'UNKNOWN')
            integrated_dataset.append(accident_list)

    return integrated_dataset
