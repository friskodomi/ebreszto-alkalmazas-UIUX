# modell/model.py
import random

class Model:
    def __init__(self):
        self.alarms = []

        # 2 tmp alarm
        self.alarms = [
            {
                "time": "07:30",
                "alarm_name": "Morning Run",
                "repeat_days": ["Mon", "Wed", "Fri"]
            },
            {
                "time": "22:00",
                "alarm_name": "Take Medication",
                "repeat_days": ["Mon"]
            }
        ]
        
    # For the Statistics View
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

    # For the Alarms View
    def save_alarm(self, alarm_data: dict):
        self.alarms.append(alarm_data)

    def get_alarms(self):
        return self.alarms