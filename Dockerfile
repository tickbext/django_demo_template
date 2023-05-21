FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 80

ENTRYPOINT ["uvicorn", "django_demo_site.asgi:application", "--port", "80", "--host", "0.0.0.0"]