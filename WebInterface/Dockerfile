FROM ubuntu:groovy

ADD . /app/
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install flask redis flask-wtf
WORKDIR /app
ENTRYPOINT ["/bin/sh", "-c", "python3 /app/WebInterface.py"]
