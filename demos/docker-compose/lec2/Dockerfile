FROM ubuntu:24.04
RUN apt-get update && apt-get install -y python3 python3-pip iproute2
COPY requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt --break-system-packages
COPY *.py /
CMD ["python3", "-u", "/server.py"]
