FROM python:3.10

WORKDIR /backend/

COPY requirements.txt .

RUN pip install -r requirements.txt

# COPY . .  # Uncomemnt in production