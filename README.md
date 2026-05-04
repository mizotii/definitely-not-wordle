# definitely-not-wordle

[definitely-not-wordle](https://definitely-not-wordle-client.onrender.com)

A minimal Wordle clone. Flask backend, React frontend.
(GoLinks 2026 Fullstack Intern Project)

## Prerequisites

- Python 3.12+
- Node.js 18+

## Backend

```bash
cd backend
python -m venv .venv
source .venv/Scripts/activate  # win: .venv\Scripts\activate
pip install -r requirements-dev.txt
```

Create `backend/.env` with:

```
SECRET_KEY=your_secret_key
FRONTEND_HOST=http://localhost:5173
FLASK_ENV=development
```

Generate a secret key with `python -c "import secrets; print(secrets.token_hex(32))"`.

```bash
flask --app server.py run
```

## Frontend

```bash
cd frontend
npm install
```

Create `frontend/.env` with:

```
VITE_API_BASE_URL=http://localhost:5000
```

```bash
npm run dev
```

## Tests

```bash
cd backend
pytest tests/ -v
```
