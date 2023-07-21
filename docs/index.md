# Cookiecutter Data Package

Project template for creation of [frictionless data packages](https://frictionlessdata.io/).

## Installation

- git
- make
- Python (with packages `cookiecutter` and `pip-tools`)
- Docker (optional)

## Usage

To create a new data package run

```bash
cookiecutter https://github.com/splor-mg/cookiecutter-datapackage.git
project_slug: project
Creating virtual environment...
Running pip compile...
Initializing Git repository...
Initialized empty Git repository in ~/project/.git/
```

```bash
cd ~/project/
source venv/bin/activate
pip install -r requirements.txt
```

### data extraction

A etapa de extração tende a ser menos genérica que as demais, podendo inclusive ser manual.

### metadata (data package, schemas and dialect)

### transform and build pipeline

### scheduled jobs

### validation and checks

### publish

## Maintenance

### Dependencies

### Secrets

- DOCKERHUB_TOKEN
- DOCKERHUB_USERNAME
