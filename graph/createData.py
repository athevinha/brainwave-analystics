
import csv
import random
import time
import os

x_value = 0
total_1 = 10

fieldnames = ["x_value", "total_1"]


with open('data.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

while True:

    with open('data.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        info = {
            "x_value": x_value,
            "total_1": total_1,
        }

        csv_writer.writerow(info)
        print(x_value, total_1)

        x_value += 1
        total_1 = random.randint(-6, 8)

    time.sleep(1)
