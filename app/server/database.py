import motor.motor_asyncio
from bson.objectid import ObjectId
import bcrypt
import jwt
import datetime

MONGO_DETAILS = "mongodb+srv://servermark332:RyhXao4ikDIoia0l@cluster0.gpydpey.mongodb.net/driver_drowsiness"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.driver_drowsiness

user_collection = database.get_collection("user_collection")
SECRET_KEY = "bounma@1234-2024"


# helpers


def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "fullname": user["fullname"],
        "lastname": user["lastname"],
        "phonenumber": user["phonenumber"],
        "email": user["email"]
       
    }


async def retrieve_user():
    users = []
    async for users in user_collection.find():
        users.append(user_helper(users))
    return users


# Add a new user into to the database
async def add_user(user_data: dict) -> dict:
    user = await user_collection.insert_one(user_data)
    new_user = await user_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)

async def register_user(user_data: dict) -> dict:
    user_data['role'] = 'user'
    
    # Hash the password
    password = user_data.get("password")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    # Replace the plain text password with the hashed password
    user_data["password"] = hashed_password
    
    # Insert the user data into the database
    user = await user_collection.insert_one(user_data)
    
    # Retrieve the newly created user data
    new_user = await user_collection.find_one({"_id": user.inserted_id})
    
    return user_helper(new_user)

async def login_user(login_data: dict) -> dict:
    phone_number = login_data.get("phonenumber")
    password = login_data.get("password")
    
    # Find the user by phone number
    user = await user_collection.find_one({"phonenumber": phone_number})
    
    if not user:
        return {"error":"Invalid phone or password"}
    if bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        token = generate_jwt_token(user)
        return token, user_helper(user)
    
    return {"error": "Invalid phone number or password"}

def generate_jwt_token(user):
    payload = {
        "_id": str(user["_id"]),
        "role": user["role"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)  # Token expires in 24 hours
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token
# Retrieve a student with a matching ID
async def retrieve_user(id: str) -> dict:
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        return user_helper(user)


# Update a student with a matching ID
async def update_user(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        updated_user = await user_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_user:
            return True
        return False


# Delete a student from the database
async def delete_user(id: str):
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        await user_collection.delete_one({"_id": ObjectId(id)})
        return True