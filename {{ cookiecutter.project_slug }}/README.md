# {{ cookiecutter.project_slug }}

[![Updated](https://github.com/splor-mg/{{ cookiecutter.project_slug }}/actions/workflows/all.yaml/badge.svg)](https://github.com/splor-mg/{{ cookiecutter.project_slug }}/actions/)

## Pré-requisitos

Esse projeto utiliza Docker para gerenciamento das dependências. Para fazer _build_  da imagem execute:

```bash
docker build --tag {{ cookiecutter.project_slug }} .
```

## Uso

Para executar o container

```bash
docker run -it --rm --mount type=bind,source=$(PWD),target=/project {{ cookiecutter.project_slug }} bash
```

Uma vez dentro do container execute os comandos do make

```bash
make all
```

_Gerado a partir de [cookiecutter-datapackage@{% gitcommit short=True%}](https://github.com/splor-mg/cookiecutter-datapackage/commit/{% gitcommit %})_
