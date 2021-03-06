FROM python:3.7

COPY poetry.lock /
COPY pyproject.toml .
RUN pip3 install poetry
RUN poetry config settings.virtualenvs.create false
RUN poetry install

COPY . /

EXPOSE 8000

CMD alembic upgrade head && \
    gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0

