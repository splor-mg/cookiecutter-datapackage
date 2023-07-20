# cookiecutter-datapackage

## Pre-requisites

- git
- make
- Python (with packages `cookiecutter` and `pip-tools`)
- Docker

## Usage

To create 

```bash
cookiecutter /Users/fjunior/Projects/splor/cookiecutter
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

