FROM tiangolo/uvicorn-gunicorn:python3.7

WORKDIR src/dgml

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

RUN python -m src.prepare_dgml_data src/config.json

#RUN conda env create -f environment.yml
#ENV PATH /opt/conda/envs/dgml/bin:$PATH
#RUN /bin/bash -c "source activate dgml"

