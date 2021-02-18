FROM ubuntu:groovy

ADD move.py /app/move.py
RUN apt-get update && apt-get install -y python3 python3-pip
RUN python3 -m pip install --upgrade pip
RUN pip3 install flask redis pyproj
WORKDIR /app
ENTRYPOINT ["/bin/sh", "-c", "python3 /app/move.py"]