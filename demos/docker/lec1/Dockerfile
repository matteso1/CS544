FROM ubuntu:24.04
RUN apt-get update && \
    apt-get install -y unzip python3 python3-pip
RUN pip3 install pandas==2.2.3 --break-system-packages
COPY test.py /test.py
CMD ["python3", "/test.py"]