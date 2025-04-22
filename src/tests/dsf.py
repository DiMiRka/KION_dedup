import json
import random

with open("test_data.json", "r", encoding="utf-8") as file:
    test_data = json.load(file)

# print(type(random.choice(test_data)))
test = json.dumps(random.choice(test_data))
print(test)

