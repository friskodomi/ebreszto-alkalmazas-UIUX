# modell/model.py
import random

class Model:
    def __init__(self):
        self.alarm_groups_data = []

        self.alarm_groups_data = [
            {
                "group_name": "Workout",
                "alarms": [
                    {"time": "06:30", "repeat_days": ["Mon", "Wed", "Fri"], "enabled": True},
                    {"time": "08:00", "repeat_days": ["Sat"], "enabled": False}
                ]
            },
            {
                "group_name": "Bedtime",
                "alarms": [
                    {"time": "22:30", "repeat_days": ["Every day"], "enabled": True}
                ]
            },
            {
                "group_name": "Medication",
                "alarms": [
                    {"time": "08:00", "repeat_days": ["Every day"], "enabled": True},
                    {"time": "20:00", "repeat_days": ["Every day"], "enabled": True}
                ]
            },
            {
                "group_name": "School",
                "alarms": [
                    {"time": "07:15", "repeat_days": ["Mon", "Tue", "Wed", "Thu", "Fri"], "enabled": True}
                ]
            },
            {
                "group_name": "Hydration Reminders",
                "alarms": [
                    {"time": "10:00", "repeat_days": ["Every day"], "enabled": False},
                    {"time": "14:00", "repeat_days": ["Every day"], "enabled": False},
                    {"time": "18:00", "repeat_days": ["Every day"], "enabled": False}
                ]
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
        self.alarm_groups_data.append(alarm_data)

    def get_alarms(self):
        return self.alarm_groups_data