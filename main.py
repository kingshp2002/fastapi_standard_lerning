from fastapi import FastAPI, status

from exceptions import EmailAlreadyExistsException, UserNotFoundException
from schemas import UserOutput, UserRequest, UserResponse

app = FastAPI()

user_list = []
# @app.get("/")
# async def read_root():
#     return user_list

@app.get("/users",response_model=list[UserOutput])
def get_users():
    return user_list

@app.post("/user",response_model=UserResponse,status_code = status.HTTP_201_CREATED)
def create_user(user: UserRequest):
    if any(user.email == u.email for u in user_list):
        raise EmailAlreadyExistsException()
    new_user = UserOutput(id=len(user_list) + 1, **user.model_dump())
    user_list.append(new_user)
    return {"message": "create user","user": new_user}



@app.get("/user/{user_id}",response_model=UserOutput)
def get_user(user_id: int):
    existing_user = next((user for user in user_list if user.id == user_id), None)
    if not existing_user:
        raise UserNotFoundException()
    return existing_user

@app.put("/user/{user_id}",response_model=UserResponse)
def update_user(user_id: int, user: UserRequest):
    existing_user = next((user for user in user_list if user.id == user_id), None)
    if not existing_user:
        raise UserNotFoundException()
    if any(user.email == u.email and u.id != user_id for u in user_list):
        raise EmailAlreadyExistsException()
    for key, value in user.model_dump().items():
        setattr(existing_user, key, value)
    return {"message": "update user","user": existing_user}

@app.patch("/user/{user_id}",response_model=UserResponse)
def partial_update_user(user_id: int, user: UserRequest):
    existing_user = next((user for user in user_list if user.id == user_id), None)
    if not existing_user:
        raise UserNotFoundException()
    if user.email and any(user.email == u.email and u.id != user_id for u in user_list):
        raise EmailAlreadyExistsException()
    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(existing_user, key, value)
    return {"message": "partial update user","user": existing_user}

@app.delete("/user/{user_id}",response_model=UserResponse)
def delete_user(user_id: int):
    existing_user = next((user for user in user_list if user.id == user_id), None)
    if not existing_user:
        raise UserNotFoundException()
    user_list.remove(existing_user)
    return {"message": "delete user","user": existing_user}