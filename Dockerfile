FROM python:3.9.1
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
