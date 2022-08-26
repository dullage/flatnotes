FROM --platform=$BUILDPLATFORM python:3.10-slim-bullseye AS build

RUN apt update && apt install -y npm

ARG BUILD_DIR=/build
RUN mkdir ${BUILD_DIR}
WORKDIR ${BUILD_DIR}

COPY package.json package-lock.json ./
RUN npm ci

COPY flatnotes/src ./flatnotes/src
RUN npm run build


FROM python:3.10-slim-bullseye

ARG USER=flatnotes
ARG UID=1000
ARG GID=1000

ARG APP_DIR=/app
ARG DATA_DIR=${APP_DIR}/data

ENV FLATNOTES_PATH=${DATA_DIR}
ENV PORT=80

RUN addgroup \
    --gid $GID \
    ${USER} \
    || echo "Group '${GID}' already exists."

RUN adduser \
    --disabled-password \
    --gecos "" \
    --ingroup ${USER} \
    --uid ${UID} \
    ${USER} \
    || echo "User '${UID}' already exists."

RUN pip install pipenv

RUN mkdir -p ${DATA_DIR}
RUN chown -R ${UID}:${GID} ${APP_DIR}
WORKDIR ${APP_DIR}

USER ${UID}

COPY --chown=${UID}:${GID} LICENSE Pipfile Pipfile.lock ./
RUN pipenv install --deploy --ignore-pipfile

COPY flatnotes ./flatnotes
COPY --from=build --chown=${UID}:${GID} /build/flatnotes/dist ./flatnotes/dist

ENTRYPOINT [ "pipenv", "run", "python", "-m", "uvicorn", "main:app", "--app-dir", "flatnotes", "--host", "0.0.0.0", "--port", "${PORT}" ]
