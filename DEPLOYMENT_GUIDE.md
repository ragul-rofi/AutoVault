# 🚀 AutoVault Free Cloud Hosting & Live Demo Guide

This guide provides step-by-step instructions to host **AutoVault** using 100% free cloud services:
- **Neon DB** (Serverless PostgreSQL Database)
- **Render** (Flask Python Backend API)
- **Vercel** (Svelte + Vite Frontend UI)

---

## 📊 Demo Login Credentials

Use these credentials during your presentation to demonstrate role-based access control (RBAC):

| Role | Email | Password | Permissions |
| :--- | :--- | :--- | :--- |
| **Admin** | `john.doe@autovault.com` | `admin123` | Full access (Upload, Rollback, Diff, User Management) |
| **Operations Manager** | `sarah.connor@autovault.com` | `ops123` | Machine Management, Upload, Rollback, Diff |
| **Senior Engineer** | `jane.smith@autovault.com` | `engineer123` | Upload files, View file versions, Diff |
| **Machine Viewer** | `bob.johnson@autovault.com` | `viewer123` | Read-only file downloads and audit trail |

---

## 🛠️ Step 1: Set Up Database on Neon DB (Free Postgres)

1. Sign up/log in at [neon.tech](https://neon.tech).
2. Click **Create Project** and name it `AutoVault`.
3. In the project dashboard, select your database string. Copy the **Connection String** (`psycopg2` / `SQLAlchemy` format):
   ```text
   postgresql://neondb_owner:npg_uBJzoh8VO7np@ep-bitter-cake-ape32uqa-pooler.c-7.us-east-1.aws.neon.tech/neondb?sslmode=require
   ```

---

## 🌾 Step 2: Seed Data into Neon DB

Before deploying the backend, seed your Neon DB with realistic manufacturing machines, file revisions, and audit logs.

Run this command in your local terminal (PowerShell / Bash) with your Neon DB connection string:

### Windows (PowerShell):
```powershell
$env:DATABASE_URL="postgresql://neondb_owner:npg_uBJzoh8VO7np@ep-bitter-cake-ape32uqa-pooler.c-7.us-east-1.aws.neon.tech/neondb?sslmode=require"
python seed.py
```

### Mac / Linux:
```bash
DATABASE_URL="postgresql://[user]:[password]@[ep-xyz].neon.tech/neondb?sslmode=require" python seed.py
```

*(You will see `Schema successfully built!`, `Users seeded!`, `Machines seeded!`, `Files and File Versions seeded!`, and `Audit logs seeded!`)*

---

## ⚙️ Step 3: Deploy Backend on Render (Free Python Web Service)

1. Log in to [render.com](https://render.com).
2. Click **New +** -> **Web Service**.
3. Connect your GitHub repository containing the AutoVault code.
4. Fill in the deployment details:
   - **Name**: `autovault-backend`
   - **Region**: Choose closest to your target audience.
   - **Branch**: `main` (or your active branch)
   - **Root Directory**: Leave blank (root of project)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn main:app`
   - **Instance Type**: `Free`
5. Add **Environment Variables** under *Advanced*:
   - `DATABASE_URL`: `postgresql://[user]:[password]@[ep-xyz].neon.tech/neondb?sslmode=require`
   - `FLASK_SECRET_KEY`: `autovault-prod-demo-secret-key-2026`
   - `PYTHON_VERSION`: `3.11.0`
6. Click **Create Web Service**.
7. Wait ~2 minutes for the build to finish. Copy your backend URL:
   `https://autovault-backend.onrender.com`

---

## 🎨 Step 4: Deploy Frontend on Vercel (Free Frontend Hosting)

1. Log in to [vercel.com](https://vercel.com).
2. Click **Add New...** -> **Project**.
3. Import your AutoVault GitHub repository.
4. Configure Project Settings:
   - **Framework Preset**: `Vite`
   - **Root Directory**: `frontend-svelte`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. Expand **Environment Variables** and add:
   - **Name**: `VITE_API_BASE_URL`
   - **Value**: `https://autovault-backend.onrender.com` *(Replace with your actual Render backend URL from Step 3)*
6. Click **Deploy**.
7. Once deployment finishes, Vercel gives you your live URL (e.g. `https://autovault.vercel.app`).

---

## 📋 Step 5: Live Demo Verification Checklist

During your company presentation today, test these features to wow the audience:

1. **Overview & Analytics**: Show machine statuses, revision depth KPI, and heatmaps.
2. **Machines & Files**: Navigate to Machine 101 (`MillAlpha`) and view version history of `pump_housing.nc`.
3. **File Comparison**: Open **Compare**, select Machine `101`, file `pump_housing.nc`, Version `1` vs `2` to view side-by-side G-Code diff highlighting.
4. **File Rollback**: Trigger a rollback of `pump_housing.nc` back to Version 1 (automatically generates Version 3 with audit entry).
5. **Audit Trail**: Switch to **Audit Trail** page to demonstrate compliance logs (UPLOAD, ROLLBACK, DIFF, DOWNLOAD).
6. **Access Control**: Log in as `john.doe@autovault.com` to manage team user roles (`admin`, `engineer`, `viewer`).

---

## 💡 Troubleshooting & Demo Tips

- **Free Tier Cold Starts**: Render's free tier spins down after 15 minutes of inactivity. Send a quick request to your backend URL (`https://autovault-backend.onrender.com`) 5 minutes before your presentation to wake it up!
- **Local Fallback Storage**: The backend automatically supports local storage fallback if MinIO is not deployed in cloud environments. File uploads, previews, downloads, and diffs work seamlessly out of the box!
