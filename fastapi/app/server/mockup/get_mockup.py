import requests
import json
from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import (
    add_water,
    delete_water,
    retrieve_water,
    retrieve_waters,
    update_water,
)
from server.models.water import (
    ErrorResponseModel,
    ResponseModel,
    WaterSchema,
    UpdateWaterModel,
)

router = APIRouter()

@router.get("/{id}", response_description="water data retrieved")
async def get_mockup_data(id):
    #url = 'http://192.168.10.159/v1/'+str(id)
    url = 'http://192.168.1.3:7078'#/'+str(id)
    mockup = requests.get(url)
    if mockup:
        print(json.loads(mockup.text))
        return ResponseModel(str(mockup.text), "API data id:" +str(id) +" retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "data doesn't exist.")


@router.get("/{id}", response_description="water data retrieved and pushed to database")
async def fetch_and_store_data(id):
    url = 'http://192.168.1.3:7078/'+str(id)
    mockup = requests.get(url)
    if mockup:
        text = mockup.json()
        text = text[0]
        date = text['w_date'].split("T")[0].split("-")
        Object: UpdateWaterModel ={
            "year":date[0],
            "date":date[1],
            "month":date[2],
            "w_height":text["w_height"],
            "w_cubic":text["w_cubic"]
        }
        print(json.loads(mockup.text))
        return await add_water(Object),ResponseModel(str(mockup.text),"API data id:" +str(id) +" retrieved successfully")
    return ResponseModel("An error occurred.", 404, "data doesn't exist.")
