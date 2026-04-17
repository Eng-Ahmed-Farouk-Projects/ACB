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

class BankAccount(pydantic.BaseModel):
    name: str
    owner_id: str
    super_admin_token: str

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

@app.post("/new_bank_account/")
def add_bank_account_form(form: BankAccount):
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO pending_accounts (name, owner_id, description) VALUES (?, ?, ?)",
                    (form.name, form.owner_id, form.description))
        conn.commit()
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

@app.get("/pending_accounts/")
def get_pending_accounts():
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, owner_id, description FROM pending_accounts")
        accounts = cursor.fetchall()
        return [{"id": account[0], "name": account[1], "owner_id": account[2], "description": account[3]} for account in accounts]
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

@app.post("/approve_account/{account_id}")
def approve_account(account_name: str, super_admin_token: str):
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        token_data = decode_token(super_admin_token)
        if not token_data.get("is_super_admin"):
            raise fastapi.HTTPException(status_code=403, detail="Only super admins can approve accounts")
        cursor.execute("SELECT name, owner_id FROM pending_accounts WHERE name = ?", (account_name,))
        account = cursor.fetchone()
        if account:
            account_id = str(uuid.uuid4())
            cursor.execute("INSERT INTO bank_accounts (id, name, balance, owner_id, created_at, members, approver) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (account_id, account[0], 0.0, account[1], datetime.datetime.now(), "[]", token_data["user_id"]))
            cursor.execute("DELETE FROM pending_accounts WHERE name = ?", (account_name,))
            conn.commit()
            return {"message": "Account approved and created successfully"}
        else:
            return {"error": "Pending account not found"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

@app.get("/bank_accounts/{account_id}")
def get_bank_account(account_id: str):
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT bank_accounts.id, bank_accounts.name, bank_accounts.balance, users.display_name, bank_accounts.created_at FROM bank_accounts JOIN users ON bank_accounts.id = users.id WHERE bank_accounts.id = ?", (account_id,))
        account = cursor.fetchone()
        if account:
            return {
                "id": account[0],
                "name": account[1],
                "balance": account[2],
                "owner_name": account[3],
                "created_at": account[4]
            }
        else:
            return {"error": "Bank account not found"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()