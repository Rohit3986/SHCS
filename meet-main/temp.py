import json
from datetime import datetime

my_datetime = datetime(2023, 5, 25, 10, 30, 0)  # Replace with your datetime object
datetime_string = my_datetime.isoformat()
json_data = json.dumps(datetime_string)

print(json_data)
