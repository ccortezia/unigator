FROM python:3.6

ENV DOCKERIZE_VERSION v0.3.0
ENV DEBIAN_FRONTEND noninteractive

RUN wget -q \
    https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

RUN apt-get update \
    && apt-get install -y postgresql-client

ADD databind /opt/proj/databind
ADD database /opt/proj/database
ADD .circleci/runtests.sh /opt/proj/.circleci/runtests.sh

RUN pip install virtualenv \
    && mkdir -p /opt/venvs \
    && virtualenv -p /usr/local/bin/python3 /opt/venvs/database-tests \
    && pip install -r /opt/proj/databind/py-sql/requirements.txt \
    && pip install -r /opt/proj/database/tests/requirements.txt

CMD ["dockerize", "-wait", "tcp://stack_db_1:5432", "/opt/proj/.circleci/runtests.sh"]
