from pydantic import BaseModel, ValidationError

class User(BaseModel):
    id: int
    name: str
    email: str

try:
    user = User(id=1, name="John Doe", email="johndoe@example.com")
    print(user.json())
except ValidationError as e:
    print(e)


"""
Валидация входных данных API

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None

@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.is_offer:
        item_dict.update({"discount": "10%"})
    return item_dict
"""

"""
Проверка наличия необязательных полей

from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str = None

user = User(id=1, name="John Doe")
print(user.json())
"""


"""
Преобразование данных

from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True

user_data = {"id": "1", "name": "John Doe", "email": "johndoe@example.com"}
user = User(**user_data)
print(user.dict())
"""


"""
Определение схемы данных

from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str

class UserSchema(BaseModel):
    name: str
    email: str

user = User(id=1, name="John Doe", email="johndoe@example.com")
user_schema = UserSchema.from_orm(user)
print(user_schema.json())
"""