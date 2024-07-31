FROM ubuntu:22.04
RUN apt-get update && \
    apt-get -y install python3 socat python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install pycryptodome

WORKDIR /home/nobody
COPY src .

USER nobody
EXPOSE 4044
CMD socat TCP-LISTEN:4044,reuseaddr,fork EXEC:"python3 -u chall.py"