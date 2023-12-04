import motor.motor_asyncio
from bson.objectid import ObjectId

MONGO_DETAILS = "mongodb://tesarally:contestor@mongoDB:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)#connect with mongoDB

database = client.Waterlevel

water_collection = database.get_collection("water_height")

def water_helper(water) -> dict:
    return {
        #"id": str(water["_id"]),
        #"name": water["name"],
        #"year": water["year"],
        #"month": water["month"],
        "date": water["date"],
        "w_height": water["w_height"],
        "w_Q3": water["w_Q3"],
        "w_H3": water["w_H3"],
    }

# Retrieve all waters present in the database
async def retrieve_waters():
    waters = []
    async for water in water_collection.find():
        waters.append(water_helper(water))
    return waters


# Add a new water into to the database
async def add_water(water_data: dict) -> dict:
    water = await water_collection.insert_one(water_data)
    new_water = await water_collection.find_one({"_id": water.inserted_id})
    return water_helper(new_water)


# Retrieve a water data with a matching ID
async def retrieve_water(id: str) -> dict:
    water = await water_collection.find_one({"_id": ObjectId(id)})
    if water:
        return water_helper(water)


# Update a water with a matching ID
async def update_water(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    water = await water_collection.find_one({"_id": ObjectId(id)})
    if water:
        updated_water = await water_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_water:
            return True
        return False


# Delete a water from the database
async def delete_water(id: str):
    water = await water_collection.find_one({"_id": ObjectId(id)})
    if water:
        await water_collection.delete_one({"_id": ObjectId(id)})
        return True
