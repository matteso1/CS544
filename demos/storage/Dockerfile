FROM ubuntu:24.04
RUN apt-get update && apt-get install -y python3 python3-pip iproute2 wget unzip
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt --break-system-packages
RUN wget https://pages.cs.wisc.edu/~harter/cs544/data/hdma-wi-2021.zip && \
    unzip hdma-wi-2021.zip && \
    rm hdma-wi-2021.zip
CMD ["python3", "-m", "jupyterlab", "--no-browser", "--ip=0.0.0.0", "--port=300", "--allow-root", "--NotebookApp.token=''"]
