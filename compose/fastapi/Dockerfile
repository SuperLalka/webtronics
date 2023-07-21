FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

ENV PYTHONPATH "${PYTHONPATH}:/"

RUN apt-get update -y \
  && apt-get install gcc -y

COPY ./app /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt
