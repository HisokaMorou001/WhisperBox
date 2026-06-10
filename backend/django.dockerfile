FROM python:3.10.4

WORKDIR /app

COPY . /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/backend

RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
