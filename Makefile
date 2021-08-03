.ONESHELL:
SHELL=/bin/bash
CONDA_ACTIVATE=source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate ; conda activate
CONFIG_FILE=./src/config/mlapi_parameters.json
.PHONY: run_prepare_dgml_data deploy_app build_docker run_prepare_dgml_data_docker deploy_app_docker run_docker

run_prepare_dgml_data:
	$(CONDA_ACTIVATE) dgml
	python -m src.prepare_dgml_data src/config.json
deploy_app:
	$(CONDA_ACTIVATE) dgml
	gunicorn app.main:server

build_docker:
	echo "Remove image"
	docker rm -f dgml
	echo "Build image"
	docker build -t dgml .

run_prepare_dgml_data_docker:
	docker rm dgml
	docker run --name dgml -v $(pwd)/dgml:/dgml dgml python -m src.prepare_dgml_data src/config.json

deploy_app_docker:
	docker rm dgml
	docker run  -p 8050:80 --env-file ./deploy_docker.env --name dgml dgml

all: run_prepare_dgml_data deploy_app
all_docker: build_docker run_prepare_dgml_data_docker deploy_app_docker
