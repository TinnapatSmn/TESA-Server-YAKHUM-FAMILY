from fastapi import APIRouter 
from fastapi import FastAPI 
from fastapi_mqtt.fastmqtt import FastMQTT
from fastapi_mqtt.config import MQTTConfig
import fastapi
import json
import pymongo
import asyncio

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

#database
MONGO_DETAILS = "mongodb://tesarally:contestor@mongodb:27017"
mongo_client  = pymongo.MongoClient(MONGO_DETAILS)
db = mongo_client["Waterlevel"]
collection = db["water_height"]

#MQTT
mqtt_config = MQTTConfig(host = "192.168.1.2",
    port= 1883,
    keepalive = 60,
    username="TGR_GROUP39",
    password="YI548E")


app = FastAPI()
router = APIRouter()

fast_mqtt = FastMQTT(config=mqtt_config)
fast_mqtt.init_app(router)


@fast_mqtt.on_connect()
def connect(client, flags, rc, properties):
    fast_mqtt.client.subscribe("/TGR_39")
    print("Connected: ", client, flags, rc, properties)
    asyncio.create_task(send_humidity_periodically())

@fast_mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    print("Received message: ",topic, payload.decode(), qos, properties)
    if topic == "/TGR_39/Hardware/receive":
        try:
            payload_dict = json.loads(payload.decode())
            w_height = payload_dict.get("w_height")
            if w_height is not None:
                document = {
                    "date": 0,
                    "w_height": w_height,
                    "w_Q3": 0.0,
                    "w_H3": 0.0
                }
                collection.insert_one(document)
                print("Inserted data to MongoDB:", document)
            else:
                print("No 'w_height' found in the payload.")
        except json.JSONDecodeError as e:
            print("Error decoding JSON payload:", e)
        except Exception as ex:
            print("An error occurred while inserting data to MongoDB:", ex)
        

@fast_mqtt.subscribe("/TGR_39/Hardware/receive")
async def message_to_topic(client, topic, payload, qos, properties):
    print("Received message to specific topic: ", topic, payload.decode(), qos, properties)
    
@fast_mqtt.subscribe("/TGR_39/Hardware/sent")
async def message_to_topic(client, topic, payload, qos, properties):
    print("Received message to specific topic: ", topic, payload.decode(), qos, properties)
    
@fast_mqtt.subscribe("/TGR_39/Matlab/sent")
async def message_to_topic(client, topic, payload, qos, properties):
    print("Received message to specific topic: ", topic, payload.decode(), qos, properties)
    
@fast_mqtt.subscribe("/TGR_39/Matlab/receive")
async def message_to_topic(client, topic, payload, qos, properties):
    print("Received message to specific topic: ", topic, payload.decode(), qos, properties)

@fast_mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")

@fast_mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)


@router.get("/", response_description="test publish to mqtt")
async def publish_hello():
    fast_mqtt.publish("/TGR_39", "Hello TGR_17")
    return {"result": True,"message":"Published" }

async def send_humidity_periodically():
    while True:
        await asyncio.sleep(60)
        fast_mqtt.publish("/TGR_39/Hardware/sent", '{"hum": true}')
        print("Sent humidity data to /TGR_39/Hardware/sent")
