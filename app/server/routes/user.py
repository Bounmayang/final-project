from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import (
    add_user,
    login_user,
    delete_user,
    retrieve_user,
    retrieve_user,
    update_user,
    register_user
)
from server.models.user import (
    ErrorResponseModel,
    ResponseModel,
    ResponseLogin,
    UserSchema,
    UserLoginSchema,
    UpdateUserModel,
)

router = APIRouter()



@router.post("/", response_description="User data added into the database")
async def add_student_data(user: UserSchema= Body(...)):
    user = jsonable_encoder(user)
    new_user = await add_user(user)
    return ResponseModel(new_user, "User added successfully.")


@router.post("/register", response_description="register into the database")
async def register_user_data(user: UserSchema= Body(...)):
    user = jsonable_encoder(user)
    new_user = await register_user(user)
    return ResponseModel(new_user, "User register successfully.")

@router.post("/login", response_description="user login")
async def login_user_data(user: UserLoginSchema= Body(...)):
    user = jsonable_encoder(user)
    print("user=====================>", user)
    token, user_data = await login_user(user)
    return ResponseLogin(user_data,token, "login successfully.")