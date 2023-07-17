from python:alpine
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
WORKDIR /app/app
CMD python manage.py runserver 0.0.0.0:80