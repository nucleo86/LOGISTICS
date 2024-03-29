# Użyj oficjalnego obrazu Python
FROM python:3.11-bullseye

# Ustaw katalog roboczy
WORKDIR /app

# Skopiuj zawartość bieżącego katalogu do kontenera
COPY . .

# Zainstaluj zależności projektu
RUN pip install --no-cache-dir -r requirements.txt

# Uruchom serwer deweloperski Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

