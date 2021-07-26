FROM tiangolo/uvicorn-gunicorn:python3.7

WORKDIR src/open_ml_app

COPY . .

RUN pip install -r requirements.txt
#RUN conda env create -f environment.yml
#ENV PATH /opt/conda/envs/open_ML/bin:$PATH
#RUN /bin/bash -c "source activate open_ML"

