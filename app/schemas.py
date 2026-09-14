from pydantic import BaseModel, ConfigDict, Field


class TaskBase(BaseModel):
    title: str


class TaskResponse(TaskBase):
    id: int
    completed: bool

    model_config = ConfigDict(from_attributes=True)


class CreateTask(TaskBase):
    pass


class UpdateTask(BaseModel):
    title: str | None = None
    completed: bool | None = None


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None


class UserResponse(UserBase):
    id: int


class UserLogin(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
