# Portuguese Flashcard App - Plan

## Cấu trúc project

```
portuguese-flashcard/
├── backend/
│   ├── main.py          # FastAPI app, các API endpoint
│   ├── models.py        # SQLAlchemy models (Topic, Word)
│   ├── database.py      # Kết nối SQLite
│   ├── seed_data.py     # Dữ liệu mẫu từ vựng
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── App.jsx      # Toàn bộ UI (TopicsPage, FlashcardPage, QuizPage)
    │   ├── App.css      # Styles
    │   └── index.css    # Global styles
    └── package.json
```

## API Endpoints (Backend - port 8000)

| Method | URL | Mô tả |
|--------|-----|-------|
| GET | /health | Kiểm tra backend sống |
| GET | /topics | Danh sách chủ đề |
| GET | /topics/{id} | Chi tiết 1 chủ đề |
| GET | /topics/{id}/words | Từ vựng theo chủ đề |
| GET | /words/quiz?topic_id=&count= | Lấy câu hỏi quiz |

## Tính năng Frontend (port 5173)

- **Trang chủ đề**: Grid các topic, mỗi topic có icon, tên, mô tả, số từ
- **Flashcard**: Lật thẻ (PT ↔ VI), thanh tiến trình, nút trước/tiếp
- **Quiz**: Chọn chủ đề, 4 đáp án, tính điểm, xem kết quả

## Công nghệ

- Backend: Python, FastAPI, SQLAlchemy, SQLite
- Frontend: React 19, Vite, CSS thuần
