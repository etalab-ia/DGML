FROM tiangolo/uvicorn-gunicorn:python3.7

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt


COPY ./ /
WORKDIR /
#RUN python -m src.prepare_dgml_data src/config.json



