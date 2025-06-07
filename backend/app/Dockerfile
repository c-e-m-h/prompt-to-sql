FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir fastapi uvicorn sqlalchemy psycopg2-binary openai passlib[bcrypt] python-dotenv pyjwt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 