FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x docker-entrypoint.sh

RUN python manage.py collectstatic --noinput

EXPOSE 8005

ENTRYPOINT ["./docker-entrypoint.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8005"]



