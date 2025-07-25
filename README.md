# AutoVault: Secure File Versioning for PLC & CNC Programs

**AutoVault** is a secure, role-based file versioning system tailored for **PLC and CNC machine shop programs**. Built with simplicity and security in mind, it acts like a GitHub for automation industries, enabling users to manage, version, and securely access critical machine program files.

---

##  Key Features

-  **Role-Based Authentication** – Admin and Operator access levels  
-  **Smart File Uploads** – Auto-versioning with SHA256 hashing  
-  **Rollback Support (Admin)** – Restore any previous version  
-  **Download & Compare (Admin)** – Get or compare versions line-by-line  
-  **Google Drive Sync** – Local sync folder for optional cloud backup  
-  **Responsive Frontend** – Clean, minimal, and mobile-friendly UI  

---

##  Tech Stack

**Backend:**  
- Python, Flask  
- PostgreSQL *(only for metadata & user info)*  
- Hashlib, Difflib, Flask-CORS  

**Frontend:**  
- HTML, CSS, JavaScript 
- localStorage for session persistence  

---

##  Setup Instructions

###  Prerequisites

- Python 3.8+  
- pip (Python package manager)  
- PostgreSQL (if using full DB features)

---

### Run the App (Local)

1. **Clone the repository & set up a virtual environment:**

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**

```bash
pip install Flask psycopg2-binary
```

3. **Update `config.py`:**

```python
# Edit the following:
DB_NAME = "autovault"
DB_USER = "postgres"
DB_PASSWORD = "your_password"
GOOGLE_DRIVE_SYNC_PATH = r"C:\AutoVault_Backups"
```

4. **Run the backend server:**

```bash
python app.py
```

Server runs at [http://localhost:5000](http://localhost:5000)

---

### Frontend Usage

- Open `login.html` in a browser  
- Login with:
  - Admin: `admin@autovault.com / adminpass`
  - Operator: `operator@autovault.com / operatorpass`
- Frontend fetches data from:  
  `http://localhost:5000` (Update `API_BASE_URL` in JS if changed)


---

##  Available API Routes

- `POST /login` – Authenticate user  
- `POST /upload` – Upload file with auto-versioning  
- `GET /files/<machine_id>` – View file history  
- `POST /rollback` – Revert to an earlier version *(Admin only)*  
- `POST /download` – Download specific version *(Admin only)*  
- `POST /diff` – Compare two versions *(Admin only)*

---


##  Contribution

Got ideas or found bugs? Open an issue or PR. Contributions are welcome!

---

##  License

This project is licensed under MIT License.
