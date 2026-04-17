import fastapi
import pydantic
from typing import Optional
import sqlite3
import datetime
import uuid
import bcrypt
import jwt
import os

SECRET_KEY = os.getenv("secret_key")
ALGORITHM = os.getenv("algorithm")

def encrypt_password(password: str):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

app = fastapi.FastAPI()

def create_token(user_id: str):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, display_name, bank_accounts, id, Email, super_admin FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    if user:
        payload = {
            "user_id": user_id,
            "username": user[0],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
            "display_name": user[1],
            "bank_accounts": user[2],
            "email": user[4],
            "is_super_admin": user[5]
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token
    else:
        fastapi.HTTPException(status_code=404, detail="User not found")

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise fastapi.HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise fastapi.HTTPException(status_code=401, detail="Invalid token")

class User(pydantic.BaseModel):
    username: str
    display_name: str
    password: str
    email: str

@app.post("/register/")
def add_user(user: User):
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        user_id = str(uuid.uuid4())
        cursor.execute("INSERT INTO users (id, username, display_name, encrypted_password, Email, created_at, bank_accounts, cards) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (user_id, user.username, user.display_name, user.password, user.email, datetime.datetime.now(), "[]", "[]"))
        conn.commit()
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

@app.get("/users/{user_id}/")
def get_user(user_id: str):
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, display_name, Email, created_at, super_admin FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        if user:
            return {
                "id": user[0],
                "username": user[1],
                "display_name": user[2],
                "email": user[3],
                "created_at": user[4],
                "is_super_admin":user[5]
            }
        else:
            return {"error": "User not found"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

@app.post("/login/")
def login(username: str, password: str):
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, encrypted_password FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        if user:
            stored_password = user[1]
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                token = create_token(user[0])
                return {"logged_in": True,"token":token, "user_id": user[0]}
        else:
            return {"logged_in": False, "error": "Invalid username or password"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()