FROM python:3.7.1
VOLUME ["/clone-root"]

COPY . /app

WORKDIR /app
RUN \
  pip install \
    poetry && \
  poetry install

CMD \
  poetry run \
    ./run.py \
      "/clone-root"
