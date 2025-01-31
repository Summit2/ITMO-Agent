FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# RUN docker compose build --no-cache

COPY . .

RUN chmod +x start.sh

CMD ["./start.sh"]
