from fastapi import FastAPI, status

from exceptions import EmailAlreadyExistsException, UserNotFoundException
from schemas import UserOutput, UserRequest, UserResponse
from services.user import UserService


app = FastAPI()

user_service = UserService()
# @app.get("/")
# async def read_root():
#     return user_list

@app.get("/users",response_model=list[UserOutput])
def get_users():
    return user_service.get_users()

@app.post("/user",response_model=UserResponse,status_code = status.HTTP_201_CREATED)
def create_user(user: UserRequest):
    new_user = user_service.create_user(user)
    return {"message": "create user","user": new_user}



@app.get("/user/{user_id}",response_model=UserOutput)
def get_user(user_id: int):
    existing_user = user_service.get_user(user_id)
    return existing_user

@app.put("/user/{user_id}",response_model=UserResponse)
def update_user(user_id: int, user: UserRequest):
    existing_user = get_user_or_404(users, user_id)
    return user_service.update_user(user_id, user)

@app.patch("/user/{user_id}",response_model=UserResponse)
def partial_update_user(user_id: int, user: UserRequest):
    existing_user = get_user_or_404(users, user_id)
    return user_service.patch_user(user_id, user)

@app.delete("/user/{user_id}",response_model=UserResponse)
def delete_user(user_id: int):
    existing_user = user_service.delete_user(user_id)
    return {"message": "delete user","user": existing_user}