# 1. image base
FROM python:3.10


WORKDIR /app
EXPOSE 8000
# 2. variaveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

#3.Diretorio de trabalho


# 4. Copiar requirements
COPY requirements.txt /app/

# 5. Instalar dependencias
RUN pip install  --upgrade pip\
    && pip install -r requirements.txt


# 6. Copiar codigo da aplicacao
COPY . /app/

# 7. Expor a porta do Django


# 8. Comando para iniciar o servidor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]