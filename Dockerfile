FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r /app/requirements.txt
COPY ./alembic.ini /app/
COPY ./alembic /app/alembic/
COPY ./src /app/src/