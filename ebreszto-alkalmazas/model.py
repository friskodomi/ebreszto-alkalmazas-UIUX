# modell/model.py
import random

class Model:
    def __init__(self):
        pass

    def get_statistics(self, period: str):
        if period == "Week":
            count = 7
        elif period == "Month":
            count = 35
        elif period == "Year":
            count = 70
        else:
            count = 1

        sleep = [round(random.uniform(5.5, 9.0), 1) for _ in range(count)]
        water = [round(random.uniform(1.5, 3.5), 1) for _ in range(count)]
        return sleep, water

    def compute_average(self, values):
        if not values:
            return 0.0
        return round(sum(values) / len(values), 2)
