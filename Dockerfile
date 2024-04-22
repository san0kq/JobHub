FROM python:3.12-alpine as requirements_stage

ENV PYTHONUNBUFFERED=1

WORKDIR /tmp

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN pip install poetry && poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.12-alpine

WORKDIR /project

COPY --from=requirements_stage /tmp/requirements.txt /project/requirements.txt

RUN pip install --upgrade pip && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r /project/requirements.txt && \
    pip install --no-cache /wheels/* \
    && rm -rf /var/lib/apt/lists/*

COPY . /project

CMD ["python3", "./src/manage.py", "runserver"]
