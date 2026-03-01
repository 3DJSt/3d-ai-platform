cd d:\code\3d-ai-platform\backend
python -m pip install fastapi uvicorn sqlalchemy pymysql pydantic pydantic-settings python-jose passlib bcrypt python-multipart alembic requests aiofiles
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
