FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
RUN python3 -c "from app import init_db; init_db()"
CMD ["python3", "app.py"]
