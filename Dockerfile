FROM python:3

LABEL maintainer="cubesiva"

COPY ./requirements.txt /app/
COPY ./pgsql-con-test.py /app/

WORKDIR /app

RUN pip install -r requirements.txt

ENV DB_USER ""
ENV DB_PASS ""
ENV DB_NAME ""

# Note that SQL_HOST is not needed IF you're connecting to
# a localhost db or Cloud SQL Proxy AND you're not using Docker on MacOS
# Docker on MacOS uses hypervisor and doesn't share network with
# the host machine even when you set -net=host

# Uncomment SQL_HOST line and specify the IP to connect to
ENV SQL_HOST ""

# passing the --auto flag to remove interactivity from the script
CMD [ "python", "pgsql-con-test.py", "--auto", "--locations=10", "--employees=100", "--dontclean" ]

