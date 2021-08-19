FROM python:3.8-slim-bullseye

ARG USER=flatnotes
ARG UID=1000
ARG GID=1000

ARG APP_DIR=/app

ARG DATA_DIR=${APP_DIR}/data
ENV FLATNOTES_PATH=${DATA_DIR}

RUN addgroup \
    --gid $GID \
    ${USER} \
 && adduser \
    --disabled-password \
    --gecos "" \
    --home ${APP_DIR} \
    --ingroup ${USER} \
    --uid ${UID} \
    ${USER}

RUN mkdir ${DATA_DIR} && chown ${UID}:${GID} ${DATA_DIR}

RUN apt update && apt install -y \
      npm \
 && rm -rf /var/lib/apt/lists/* \
 && pip install pipenv

USER ${UID}
WORKDIR ${APP_DIR}

COPY --chown=${UID}:${GID} LICENSE Pipfile Pipfile.lock package.json package-lock.json ./
RUN pipenv install --system --deploy --ignore-pipfile \
 && npm ci

COPY --chown=${UID}:${GID} flatnotes ./flatnotes
RUN npm run build

ENTRYPOINT [ "python", "-m", "uvicorn", "main:app", "--app-dir", "flatnotes", "--host", "0.0.0.0", "--port", "80" ]
