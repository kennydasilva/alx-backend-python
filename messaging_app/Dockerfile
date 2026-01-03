# 1. Base image
FROM python:3.10

WORKDIR /app

# Expose Django port
EXPOSE 8000

# docker run -p 8000:8000 messaging_app

# 2. Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Copy requirements
COPY requirements.txt /app/

# 4. Install dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# 5. Copy application code
COPY . /app/

# 6. Run server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
