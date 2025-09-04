# Notes API (FastAPI)

Simple CRUD + shareable public links for notes. Uses SQLite via SQLAlchemy.

## Run locally
```bash
pip install -r requirements.txt
export PORT=8000
export DATABASE_URL=sqlite:///./notes.db
export ALLOWED_ORIGINS=http://localhost:5173
uvicorn app.main:app --host 0.0.0.0 --port $PORT --reload
```
Open http://localhost:8000/docs

## Deploy
- **Render**: uses `render.yaml` or create a Web Service with start command:
  `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Railway/Heroku/Fly.io**: use `Procfile` or similar start command.

### Env vars
- `PORT` (default 8000 on local)
- `DATABASE_URL` (e.g., `sqlite:///./notes.db` or PostgreSQL URL)
- `ALLOWED_ORIGINS` (comma-separated list of allowed frontends, e.g., your Vercel URL)
- `BASE_PUBLIC_URL` (optional, e.g., `https://api.example.com`, used to build share URLs)
