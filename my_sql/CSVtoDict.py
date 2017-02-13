#CSVtoDict

import csv

def csv_dict(file):
    with open(file) as csvfile:
        asset_list = []
        reader = csv.DictReader(csvfile)
        for row in reader:
            asset_list.append(row)
        return asset_list