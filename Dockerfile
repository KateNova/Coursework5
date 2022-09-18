FROM python:3.8.5

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY main application
COPY templates templates
COPY data data
COPY app.py .
COPY wsgi.py .