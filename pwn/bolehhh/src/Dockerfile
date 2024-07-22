FROM ubuntu:latest

RUN apt-get update 
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /etc/xinetd.d/*

RUN useradd -U -m -s /bin/bash bolehhh

WORKDIR /home/bolehhh

COPY ./flag.txt .
COPY ./chall .
COPY ./ynetd /usr/bin/ynetd

RUN chown -R root:bolehhh /home/bolehhh
RUN chmod -R 750 /home/bolehhh && chmod 440 flag.txt 
RUN mv flag.txt flag-$(md5sum flag.txt | awk '{print $1}').txt
RUN chown root:bolehhh /usr/bin/ynetd
RUN chmod 750 /usr/bin/ynetd

EXPOSE 11101

CMD ["/usr/bin/ynetd", "-p", "11101", "/home/bolehhh/chall"]
