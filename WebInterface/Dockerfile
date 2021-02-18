FROM ubuntu:bionic

ADD entityManager.py /app/entityManager.py
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install flask redis
WORKDIR /app
ENTRYPOINT ["/bin/sh", "-c", "python3 /app/entityManager.py"]