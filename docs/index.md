# Intro

Project template para criação de [frictionless data packages](https://frictionlessdata.io/).

## Requirements

Para inicialização do projeto os seguintes softwares são necessários:

- git;
- make;
- Python (e pacote `cookiecutter` e `pip-tools`).

Para execução das etapas do processo de ETL é necessário:

- Rstudio & R; ou
- Docker.

## Quickstart

Para iniciar um novo _data package_ execute:

```bash
cookiecutter https://github.com/splor-mg/cookiecutter-datapackage
```

Depois de informar uma _slug_ para o projeto uma nova pasta será inicializada:

```bash
Creating virtual environment...
Running pip compile...
Initializing Git repository...
Initialized empty Git repository in ~/project/.git/
```

Para execução local é necessário a instalação das dependências do python no ambiente virtual do projeto:

```bash
cd ~/project/
source venv/bin/activate
pip install -r requirements.txt
```

Você pode testar que tudo funcionou com o comando:

```bash
make all
```

Que deve gerar o seguinte resultado:

```bash
python main.py extract fact && python main.py extract dim && true
2023-07-21T09:18:09-0300 INFO  [scripts.extract] Extract not implemented for resource {resource_name}...
2023-07-21T09:18:09-0300 INFO  [scripts.extract] Extract not implemented for resource {resource_name}...
frictionless validate datapackage.yaml
──────────────────────────────────────────────── Dataset ─────────────────────────────────────────────────
                   dataset                   
┏━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┓
┃ name ┃ type  ┃ path              ┃ status ┃
┡━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━┩
│ fact │ table │ data-raw/fact.txt │ VALID  │
│ dim  │ table │ data-raw/dim.txt  │ VALID  │
└──────┴───────┴───────────────────┴────────┘
python main.py transform fact --target-descriptor logs/transform/fact.json
2023-07-21T09:18:09-0300 INFO  [scripts.transform] Transforming resource fact
python main.py transform dim --target-descriptor logs/transform/dim.json
2023-07-21T09:18:10-0300 INFO  [scripts.transform] Transforming resource dim
python main.py build
frictionless validate datapackage.json
─────────────────────────────────────────────────────────── Dataset ────────────────────────────────────────────────────────────
                   dataset                   
┏━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┓
┃ name ┃ type  ┃ path              ┃ status ┃
┡━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━┩
│ fact │ table │ data/fact.csv     │ VALID  │
│ dim  │ table │ data/dim.csv      │ VALID  │
└──────┴───────┴───────────────────┴────────┘
```

Para entender como customizar o projeto siga o [Tutorial](tutorial.md).
