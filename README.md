# Cloud Storage API

A secure backend API for uploading, storing, and managing files.
Built with FastAPI, PostgreSQL, and JWT authentication, this project simulates a simplified cloud storage system similar to Dropbox or Google Drive.


# Live Demo

API Base URL:
https://cloud-storage-api-ca5o.onrender.com

Interactive API Docs:
https://cloud-storage-api-ca5o.onrender.com/docs


# Features

* User registration and login
* JWT-based authentication
* Secure file upload and storage
* User-specific file access (no cross-user access)
* File download and deletion
* File validation (size and type restrictions)
* Clean API responses using Pydantic schemas

## Authentication

Protected endpoints require a JWT token.

1. Login via `/login`
2. Copy the `access_token`
3. Click **Authorize** in `/docs`
4. Enter:

```
Bearer YOUR_TOKEN
```

## API Endpoints

### Auth

* `POST /create-user` → Register a new user
* `POST /login` → Get access token

# Files (Protected)

* `POST /upload` → Upload file
* `GET /files` → List user files
* `GET /download/{file_id}` → Download file
* `DELETE /delete/{file_id}` → Delete file

---

# Tech Stack

* FastAPI (backend framework)
* PostgreSQL (database)
* SQLAlchemy (ORM)
* JWT (authentication)
* Uvicorn (ASGI server)

---

# Local Setup

```bash
git clone https://github.com/your-username/cloud-storage.git
cd cloud-storage
pip install -r requirements.txt
```

Set environment variables:

```bash
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key (randomized string)
```

Run the server:

```bash
uvicorn app.main:app --reload
```

---

# Deployment

Deployed on Render with a cloud PostgreSQL database (Neon).

---

# Ideas For Future Improvements

* Frontend dashboard (React)
* File previews (images/PDF)
* AWS S3 integration for scalable storage
* Rate limiting and abuse protection
* Pagination for large file lists

---

# Author

Alexander Guzy
GitHub: https://github.com/alexanderjguzy

---
