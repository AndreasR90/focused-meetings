FROM python:3.10

WORKDIR /code

COPY Pipfile /code/Pipfile
COPY Pipfile.lock /code/Pipfile.lock
COPY app app
RUN pip install --no-cache-dir --upgrade pipenv

RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install uvicorn

ENV PATH="/code/.venv/bin:$PATH"

WORKDIR /code/app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
