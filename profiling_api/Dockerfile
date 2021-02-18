FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

WORKDIR /app

COPY ./ /app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

