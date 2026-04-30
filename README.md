# ACB 

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Railway](https://img.shields.io/badge/deployed%20on-Railway-131415.svg)](https://railway.app/)

<img width="1366" height="642" alt="image" src="https://github.com/user-attachments/assets/d95a429d-2d6b-4068-a0ba-67bb9eb94ab7" />

**Adapt Community Bank (Wink Wink) . a platform to support Startups to manage their Money in Egypt Under a legal framework.**
---

## Features

### For Organization Members
- **Organization Dashboard** – See balance, members, and transactions
- **Internal Transfers** – Send and receive money between different Organization
- **Donation** – Donate funds from another source
- **Transactions** – See the Full history of Recent Transactions
  
### For Super Admins
- **Organization Approvals** – Review and approve or reject new organizations


---

## Project Structure

```

ACB/
├── backend/
│   ├── main.py              # FastAPI application with all endpoints
│   ├── setup.py             # Database Creation and super admin
│   ├── requirements.txt     # Python requirements
│   └── database.db          # SQLite database (created at runtime)
├── front end/
│   ├── login/               # Login page
│   │   ├── login.html
│   │   ├── login.css
│   │   └── login.js
│   ├── register/            # Registration page
│   │   ├── register.html
│   │   ├── register.css
│   │   └── register.js
│   ├── dashboard/           # User dashboard
│   │   ├── dashboard.html
│   │   ├── dashboard.css
│   │   └── dashboard.js
│   ├── organization/        # Organization Dashboard
│   │   ├── organization.html
│   │   ├── organization.css
│   │   └── organization.js
│   ├── create_organization/ # New organization form page
│   │   ├── create_organization.html
│   │   ├── create_organization.css
│   │   └── create_organization.js
│   └── super_admin/         # Super admin panel for approvals
│       ├── super_admin.html
│       ├── super_admin.css
│       └── super_admin.js
└── README.md # that's what yo are reading right now!

```

---
## How to try 
go to : https://eng-ahmed-farouk-backup.github.io/ACB/front%20end/login/login.html

if you want to log in as a suped admin :

username : ziad_elhusiny

(thanks for allowing me to use your name lol) -(I will use Max name in the next project like I did in the last one)

Password : 12345678

that's it have fun !

## How to try (DEVELOPER MODE)

### Backend Setup

1. **Clone the Repo**
```bash
git clone https://github.com/Eng-Ahmed-Farouk-backup/ACB.git
cd ACB
```

2. **go to backend folder**
```bash
cd backend
```

3. **Install the requirements**
```bash
pip install -r requirements.txt
```

5. **Create the database**
```bash
python setup.py
```
default super admin account:
- Username: `ziad_elhusiny` # my Best friend's name , Love uuuuuuuuuuu!
- Password: `12345678`

6. **Run the backend server**
```bash
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. **go to frontend Folder**
```bash
cd ../front\ end
```

3. **Open the application**
Open with a local server:
```bash
# Using Python
python -m http.server 5500

# Using VS Code Live Server (port 5500)
```
- open: `http://localhost:5500/login/login.html`

---
# Logo 
I made this Logo using Canva but Didn't put it on the Website becuase this is the 1st logo Draft 
<img width="2000" height="2000" alt="ACB Branding (1)" src="https://github.com/user-attachments/assets/f6cae190-7a42-4ee3-b9f3-63c7a00a8b4d" />

# Author
this is Platform Made By Ahmed Farouk
Passionate about STEAM, Entrepreneurship 

- Leader of Innovations Hack Club
- Founder & CEO of Adapt Community
- Present Contractor @ Hack club under the Management of Christina (the co founder)
