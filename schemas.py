from pydantic import BaseModel , Field,EmailStr

class UserRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=50,description="The name of the user")
    age: int = Field(..., gt=1, lt=100,description="The age of the user")
    email: EmailStr = Field(..., description="The email of the user")
    password: str = Field(..., min_length=8, max_length=64,description="The password of the user")


class UserOutput(BaseModel):
    id: int = Field(..., description="The id of the user")
    name: str = Field(..., description="The name of the user")
    age: int = Field(..., description="The age of the user")
    email: EmailStr = Field(..., description="The email of the user")


class UserResponse(BaseModel):
    message: str = Field(..., description="The message of the user")
    user: UserOutput = Field(..., description="The user of the user")