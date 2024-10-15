FROM python:3.11-slim AS requirements-stage

WORKDIR /tmp

RUN pip install poetry==1.8.3

COPY poetry.lock pyproject.toml /tmp/

RUN poetry export -f requirements.txt --output requirements.txt

FROM python:3.11-slim

WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /code/