.ONESHELL:
SHELL=/bin/bash
.PHONY: install venv run_prepare_dgml_data deploy_app build_docker run_prepare_dgml_data_docker deploy_app_docker run_docker
VENV_NAME = dgml_venv

install: venv
	. $(VENV_NAME)/bin/activate && pip install -r requirements.txt

venv:
	test -d $(VENV_NAME) ||  virtualenv -p python3 $(VENV_NAME)

run_prepare_dgml_data:
	. $(VENV_NAME)/bin/activate && pip -V
	python -m src.prepare_dgml_data src/config.json
deploy_app:
	. $(VENV_NAME)/bin/activate && pip -V
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
	docker run  -d -p 8050:80 --env-file ./deploy_docker.env --name dgml dgml
	echo "Go to http://localhost:8050/dgml"

all: install
all_local: run_prepare_dgml_data deploy_app
all_docker: build_docker run_prepare_dgml_data_docker deploy_app_docker
