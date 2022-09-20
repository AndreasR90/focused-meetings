FROM python:3.10

# backend
WORKDIR /backend

COPY backend/Pipfile Pipfile
COPY backend/Pipfile.lock Pipfile.lock
COPY backend/app app
RUN pip install --no-cache-dir --upgrade pipenv

RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install uvicorn

ENV PATH="/backend/.venv/bin:$PATH"

# frontend
WORKDIR /frontend
RUN apt-get update
RUN  apt-get install -y nodejs npm
COPY frontend/ .
# RUN npm run build


WORKDIR /
COPY build.sh .
RUN chmod u+x build.sh
EXPOSE 80
CMD ["/build.sh"]
ENTRYPOINT [ "/bin/bash" ]
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
