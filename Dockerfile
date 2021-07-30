FROM tiangolo/uvicorn-gunicorn:python3.7

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

# WORKDIR ../

COPY ./ /
WORKDIR /app
#RUN conda env create -f environment.yml
#ENV PATH /opt/conda/envs/dgml/bin:$PATH
#RUN /bin/bash -c "source activate dgml"

