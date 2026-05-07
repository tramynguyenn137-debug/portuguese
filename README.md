# 🇧🇷 Portuguese Flashcard App

App học từ vựng tiếng Bồ Đào Nha với flashcard và quiz tương tác.

**Live URL:** https://portuguese-eight.vercel.app

## Tính năng

- **Flashcard** — lật thẻ xem nghĩa tiếng Việt, có ví dụ câu
- **Quiz** — trắc nghiệm 4 đáp án, tính điểm kết quả
- **6 chủ đề**: Chào hỏi, Số đếm, Màu sắc, Đồ ăn, Gia đình, Thời gian

## Tech Stack

| Layer | Công nghệ |
|-------|-----------|
| Frontend | React 19, Vite |
| Backend | Python, FastAPI |
| Database | PostgreSQL (Railway) |
| Deploy Frontend | Vercel |
| Deploy Backend | Railway |

## Cấu trúc project

```
portuguese-flashcard/
├── backend/
│   ├── main.py          # API endpoints
│   ├── models.py        # Database models
│   ├── database.py      # DB connection
│   ├── seed_data.py     # Dữ liệu từ vựng mẫu
│   ├── requirements.txt
│   └── railway.toml
├── frontend/
│   ├── src/
│   │   ├── App.jsx      # Toàn bộ UI
│   │   └── App.css      # Styles
│   ├── package.json
│   └── railway.toml
├── PLAN.md
├── CLAUDE.md
└── README.md
```

## Chạy local

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
# → http://localhost:8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
# → http://localhost:5173
```

## API Endpoints

| Method | URL | Mô tả |
|--------|-----|-------|
| GET | /health | Kiểm tra server |
| GET | /topics | Danh sách chủ đề |
| GET | /topics/{id}/words | Từ vựng theo chủ đề |
| GET | /words/quiz | Câu hỏi quiz ngẫu nhiên |
