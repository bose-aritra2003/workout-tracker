import os
import requests
import datetime

APP_ID = os.environ.get("APP_ID")
API_KEY = os.environ.get("API_KEY")
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")

GENDER = "male"
WEIGHT_KG = 95
HEIGHT_CM = 187.96
AGE = 19

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = "https://api.sheety.co/a1d76ac594c898091c890076a060d011/workoutTracker/workouts"

nutritionix_headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}
sheety_headers = {
    "Authorization": f"Bearer {BEARER_TOKEN}"
}
exercise_params = {
    "query": input("What exercises did you do today ?\n"),
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

data = requests.post(url=exercise_endpoint, json=exercise_params, headers=nutritionix_headers).json()
# print(data)

data_inputs = None
for exercise in data['exercises']:
    data_inputs = {
        "workout": {
            "date": datetime.datetime.now().strftime("%d/%m/%Y"),
            "time": datetime.datetime.now().strftime("%X"),
            "exercise": exercise["name"].title(),
            "duration (min)": str(exercise["duration_min"]),
            "calories": exercise["nf_calories"]
        }
    }
    sheet_response = requests.post(url=sheet_endpoint, json=data_inputs, headers=sheety_headers)
    print(sheet_response.text)
