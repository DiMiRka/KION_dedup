FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN alembic upgrade head

COPY . .

CMD ["python", "src/main.py", "--host", "0.0.0.0", "--port", "8000"]
