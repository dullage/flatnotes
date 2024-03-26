ARG BUILD_DIR=/build

# Build Container
FROM --platform=$BUILDPLATFORM python:3.11-slim-bullseye AS build

ARG BUILD_DIR

RUN mkdir ${BUILD_DIR}
WORKDIR ${BUILD_DIR}

RUN apt update && apt install -y npm

COPY package.json package-lock.json .htmlnanorc ./
RUN npm ci

COPY client ./client
RUN npm run build

# Runtime Container
FROM python:3.11-alpine3.19

ARG BUILD_DIR

ENV PUID=1000
ENV PGID=1000

ENV APP_PATH=/app
ENV FLATNOTES_PATH=/data

RUN mkdir -p ${APP_PATH}
RUN mkdir -p ${FLATNOTES_PATH}

RUN apk add --no-cache su-exec curl

RUN pip install --no-cache-dir pipenv

WORKDIR ${APP_PATH}

COPY LICENSE Pipfile Pipfile.lock ./
RUN pipenv install --deploy --ignore-pipfile --system && \
    pipenv --clear

COPY server ./server
COPY --from=build ${BUILD_DIR}/client/dist ./client/dist

VOLUME /data
EXPOSE 8080/tcp
HEALTHCHECK --interval=60s --timeout=10s CMD curl -f http://localhost:8080/health || exit 1

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]
