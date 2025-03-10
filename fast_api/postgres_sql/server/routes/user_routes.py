from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


from models.todo_model import Users
from config.database import get_db
from controllers.user_controllers import UserCreate, UserLogin
from utils.utils import create_access_token


user_routes = APIRouter()

@user_routes.post('/register')
def register(user:UserCreate, db:Session=Depends(get_db)):
    valid_user = Users(name=user.name, email=user.email, password=user.password)
    db.add(valid_user)
    db.commit()
    db.refresh(valid_user)
    return {
        "data":valid_user,
        "message":"Register Successfully",
        "status":"success"
    }

@user_routes.post('/login')
def login(user:UserLogin, db:Session=Depends(get_db)):
    db_user = db.query(Users).filter(Users.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=400,detail="User Not Found")
    if db_user.password != user.password:
        raise HTTPException(status_code=401, detail="Password not match")
    token = create_access_token(data={"sub":db_user.email,'user_id':db_user.id})
    user_data = {
        "name":db_user.name,
        "email":db_user.email,
        "password":db_user.password,
        "token":token
    }
    return {
        "data":user_data,
        "message":"User Login Successfully",
        "status":"success"
    }