# CLAUDE.md

Tài liệu này hướng dẫn Claude Code làm việc với project này.

## Project Overview

App học từ vựng tiếng Bồ Đào Nha — full-stack với FastAPI backend và React frontend.

## Cấu trúc

- `backend/` — FastAPI app, chạy port 8000
- `frontend/` — React + Vite app, chạy port 5173

## Commands

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

**Backend:**
- `DATABASE_URL` — PostgreSQL connection string
- `ALLOWED_ORIGINS` — CORS origins (vd: `https://portuguese-eight.vercel.app`)

**Frontend:**
- `VITE_API_URL` — URL của backend (vd: `https://backend-production-xxxx.up.railway.app`)

## Deploy

- Frontend: Vercel — https://portuguese-eight.vercel.app
- Backend: Railway (project balanced-nourishment)
- Database: PostgreSQL trên Railway

## Lưu ý

- `seed_data.py` chạy tự động khi backend khởi động — không cần seed thủ công
- Database dùng SQLAlchemy, hỗ trợ cả SQLite (local) và PostgreSQL (production)
- CORS được cấu hình qua env var `ALLOWED_ORIGINS`
