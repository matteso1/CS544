FROM ubuntu:24.04
RUN apt-get update && apt-get install -y python3 python3-pip curl iproute2
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt --break-system-packages
CMD ["python3", "-m", "jupyterlab", "--no-browser", "--ip=0.0.0.0", "--port=????", "--allow-root", "--NotebookApp.token=''"]
