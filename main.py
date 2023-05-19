import datetime
import random
import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic.schema import date
from sklearn.preprocessing import PolynomialFeatures
import requests
import json
from tools import  format_result

model_clone = joblib.load('model.pkl')

app = FastAPI()

API_URL = "https://dmtload.azurewebsites.net"

PROXIES = {"http": "http://grv2ct:Vbg25012023@@rb-proxy-ca1.bosch.com:8080",
           "https": "http://grv2ct:Vbg25012023@@rb-proxy-ca1.bosch.com:8080"
           }




@app.get("/data/{ref_code}")
async def predict(ref_code: str):
    id = random.randint(4, 19)
    print(ref_code)
    # if ref_code == "":
    #     id = random.randint(0, 10)
    # else:
    #     id = random.randint(11, 20)

    # response = requests.get(f"{API_URL}/StationProduct/getStationProduct/{id}", headers={}, proxies=PROXIES)
    response = requests.get(f"{API_URL}/StationProduct/getStationProduct/{id}", headers={})
    if response.status_code >= 400:
        raise HTTPException(status_code=400)

    data_product = response.json()
    predict = model_clone.predict(np.array(data_product["angulo"]).reshape(-1, 1))

    predict = format_result(predict, data_product)
    print(predict)
    print(data_product["torque"])

    data = {
            "id": 0,
            "torqueForeseen": predict,
            "torqueReal": data_product["torque"],
            "creationDate": json.dumps(datetime.datetime.now(), default=str).replace(' ', 'T').replace('"', ""),
            "idStationProduct": id,
           }
    # json.dumps(datetime.datetime.now(), default=str).replace(" ", "T")

    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json'
    }

    # response = requests.post(API_URL + f"/Story/register", json=data, headers=headers,
    #                          proxies=PROXIES)
    response = requests.post(API_URL + f"/Story/register", json=data, headers=headers)

    print(response.status_code)
    print(response)
    if response.status_code == 200:
        return True

    return False
