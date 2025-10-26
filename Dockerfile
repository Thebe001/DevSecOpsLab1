# Dockerfile pour ton app Python
FROM python:3.9-slim

WORKDIR /app
COPY . /app

# Installer les dépendances si requirements.txt existe
RUN pip install --upgrade pip && \
    if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

EXPOSE 8000

CMD ["python", "app.py"]
