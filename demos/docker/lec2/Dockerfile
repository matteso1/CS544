FROM ubuntu
RUN apt-get update && \
    apt-get install -y unzip python3 python3-pip
RUN pip3 install pandas==2.3.3 --break-system-packages
COPY ./myapp.py /myapp.py
CMD ["python3", "/myapp.py"]
