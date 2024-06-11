# Intro

Project template para criação e atualização de [frictionless data packages](https://frictionlessdata.io/) das fontes de dados primárias utilizadas no âmbito da Assessoria de Inteligência de Dados.

## Requirements

Para inicialização do projeto os seguintes softwares são necessários:

- git;
- make;
- Python (e pacotes `cookiecutter`, `jinja2-git`, e `uv` preferencialmente instalados com [`pipx`](https://github.com/pypa/pipx)).

Para execução das etapas do processo de ETL é necessário:

- Rstudio & R; ou
- Docker.

## Quickstart

Para iniciar um novo _data package_ execute:

```bash
python -m cookiecutter https://github.com/splor-mg/cookiecutter-datapackage
```

Depois de informar uma _slug_ para o projeto uma nova pasta será inicializada:

```bash
Creating virtual environment...
Running pip compile...
Initializing Git repository...
Initialized empty Git repository in ~/project/.git/
```

Agora pode ser um bom momento para fazer um commit dos arquivos originais do template:

```bash
cd ~/project/
git add .
git add -f data/.gitkeep data-raw/.gitkeep
git commit -m "initial commit"
```

!!! note

    O `cookiecutter-datapackage` possui um [workflow padronizado](https://github.com/splor-mg/cookiecutter-datapackage/blob/main/%7B%7B%20cookiecutter.project_slug%20%7D%7D/.github/workflows/all.yaml) do [Github Actions](https://docs.github.com/en/actions) para executar os _phony targets_ `make all` e `make publish` diariamente (`on schedule`) e sob demanda (`on workflow_dispatch`).

    __Ao criar um novo repositório no Github esse workflow vai estar ativo por padrão.__
    
    Se o agendamento diário não for necessário (como por exemplo em repositórios _upstream_) lembre-se de [desativar o Github Actions](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository) para esse repositório.


Para execução local é necessário a instalação das dependências do python no ambiente virtual do projeto:

```bash
source venv/bin/activate
python -m pip install -r requirements.txt
```

!!! note

    O arquivo `requirements.in` é utilizado para controle das dependências python diretas do projeto. Qualquer atualização neste arquivo deve ser seguida da execução do comando:

    ```bash
     uv pip compile requirements.in > requirements.txt
    ```

    Dessa forma o arquivo `requirements.txt` vai estar atualizado com todas as versões das dependências diretas e indiretas do projeto.

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
