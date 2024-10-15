from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

users = []

class User(BaseModel):
    id: int
    username: str
    age: int

@app.get('/')
async def read_root() -> str:
    return "Welcome to my first Management API!"

@app.get('/users', response_model=List[User])
async def get_users() -> List[User]:
    return users

@app.post('/user/', response_model=User)
def create_user(user: User) -> User:
    if any(u.id == user.id for u in users):
        raise HTTPException(status_code=400, detail="User with this ID already exists")
    users.append(user)
    return user

@app.put('/user/{user_id}', response_model=User)
async def update_user(user_id: int, updated_user: User) -> User:
    for index, user in enumerate(users):
        if user.id == user_id:
            users[index] = updated_user
            return updated_user
    raise HTTPException(status_code=404, detail='User not found')

@app.delete('/user/{user_id}')
def delete_user(user_id: int) -> str:
    for index, user in enumerate(users):
        if user.id == user_id:
            users.pop(index)
            return f'User {user_id} has been deleted'
    raise HTTPException(status_code=404, detail='User not found')




