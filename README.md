# Gmail Schedule Watcher

Schedule Gmail messages for specific threads and automatically cancel them if a new email arrives in that thread.

## Project Structure

```
├── backend/                # FastAPI backend
│   ├── app/
│   │   ├── db/             # SQLAlchemy models & session
│   │   ├── celery_app.py   # Celery configuration
│   │   └── tasks.py        # Background tasks
│   ├── alembic/            # Database migrations
│   ├── main.py             # API entry point
│   └── requirements.txt
├── frontend/               # Next.js frontend
│   └── src/
└── README.md
```

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL
- Redis

## Getting Started

### Backend (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file with:
# DATABASE_URL=postgresql://user:pass@localhost/gmail_scheduler
# REDIS_URL=redis://localhost:6379/0
# GOOGLE_CLIENT_ID=your_client_id
# GOOGLE_CLIENT_SECRET=your_client_secret

# Run migrations
alembic upgrade head

# Start API
uvicorn main:app --reload
```

API runs at: http://localhost:8000

### Celery Worker

```bash
cd backend
celery -A app.celery_app worker --loglevel=info
```

### Frontend (Next.js)

```bash
cd frontend
npm install
npm run dev
```

App runs at: http://localhost:3000

## Google API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the Gmail API
4. Create OAuth 2.0 credentials
5. Add credentials to `backend/.env`

## Features (TODO)

- [ ] Google OAuth authentication
- [ ] View Gmail threads
- [ ] Schedule messages for threads
- [ ] Auto-cancel scheduled messages on new email in thread
- [ ] Manage scheduled messages
