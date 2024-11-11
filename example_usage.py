from datetime import datetime, date, time, timedelta
import json
import random

from object_condition_checker import ObjectCondition, ConditionList


def generate_random_datetimes(start_date, end_date, num_dates=10):
    # Convert start_date and end_date to datetime objects
    start = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)

    # Calculate the total range in seconds between start and end dates
    total_seconds = int((end - start).total_seconds())

    # Generate a list of random datetimes within the range
    random_datetimes = [
        start + timedelta(seconds=random.randint(0, total_seconds)) for _ in range(num_dates)
    ]
    return random_datetimes

# Generate 10 random dates between 2022-01-01 and 2023-12-31

static_dates = generate_random_datetimes("2022-06-01", "2023-01-01", 20)

static_words = [
    "apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew",
    "kiwi", "lemon", "mango", "nectarine", "orange", "papaya", "quince", "raspberry",
    "strawberry", "tangerine", "ugli", "vanilla", "watermelon", "xigua", "yam", "zucchini",
]

class Checker:
    def __init__(self, name):
        self.name = name
        two_dates = (random.choice(static_dates), random.choice(static_dates))
        self.start_date = min(two_dates)
        self.end_date = max(two_dates)
        self.word_list = []
        for _ in range(random.randint(2, 8)):
            self.word_list.append(random.choice(static_words))
        self.sentence = "".join([random.choice(self.word_list)+" " for _ in range(random.randint(1, 5))])



or_list = []
for item in ["strawberry", "cherry", "tomato", "watermelon", "grapefruit"]:
    or_list.append(ObjectCondition("word_list", "in", item))
    or_list.append(ObjectCondition("sentence", "in", item))

reds = ConditionList(*or_list, operator="or")

between = ConditionList(ObjectCondition("start_date", "<=", "2022-01-01", value_type="date"),
ObjectCondition("end_date", ">=", "2022-12-31", value_type="date")
, operator="and")

checker_list =[]
for i in range(random.randint(4, 10)):
    checker_list.append(Checker("checker"+str(i)))


for che in checker_list:
    print("------ " + che.name + " ------")
    print(che.__dict__)
    print(reds.is_true(che))
    print(between.is_true(che))
