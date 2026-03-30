# 🔐 User Authentication Backend (FastAPI)

A secure and scalable **User Authentication Backend** built using **FastAPI**, **PostgreSQL**, and **SQLAlchemy (Async)**.  
This project implements **JWT-based authentication**, **email verification**, **password reset**, and **role-based access control** following industry best practices.

---

## 🚀 Features

- User Registration
- Email Verification (Token-based)
- Login with JWT Authentication
- Access & Refresh Token System
- Forgot Password / Reset Password via Email
- Password Hashing (bcrypt)
- Token Blacklisting (Logout support)
- Role-based User Management (Admin/User)
- Async PostgreSQL Database Support
- Secure & Modular Project Structure

---

## 🛠️ Tech Stack

| Layer | Technology |
|-----|-----------|
| Backend | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy (Async) |
| Authentication | JWT (OAuth2 Password Flow) |
| Security | bcrypt, token expiry |
| Email | SMTP (Email verification & reset) |
| Server | Uvicorn |

---

## 📁 Project Structure

app/
   api/
      v1/ 
        routers
    core/
    models/
    schemas/
    services/
    utils/
    main.py
    .env 
    requirements.txt


---

## 🔑 Authentication Flow

1. **Register User**
   - Creates user
   - Sends email verification link

2. **Verify Email**
   - Token validated
   - Account activated

3. **Login**
   - JWT Access Token generated

4. **Forgot Password**
   - Reset link sent to email

5. **Reset Password**
   - Token validation
   - Password update

6. **Logout**
   - Token blacklisted

---

## 🧪 API Endpoints (Sample)

| Method | Endpoint | Description |
|------|---------|------------|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login user |
| GET | `/auth/verify-email` | Email verification |
| POST | `/auth/forgot-password` | Send reset email |
| POST | `/auth/reset-password` | Reset password |
| POST | `/auth/logout` | Logout user |

---

## ⚙️ Environment Variables

Create a `.env` file:

DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your_email@gmail.com

EMAIL_PASSWORD=your_app_password


