FROM ubuntu:24.04
RUN apt-get update && apt-get install -y python3 python3-pip curl iproute2 wget unzip software-properties-common
RUN add-apt-repository -y ppa:deadsnakes/ppa && apt-get update && apt-get install -y python3.13-nogil python3.13-dev libffi-dev

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3.13-nogil get-pip.py

COPY requirements.txt /tmp/requirements.txt
RUN python3.13 -m pip install -r /tmp/requirements.txt --break-system-packages
RUN python3.13-nogil -m pip install ipykernel
RUN python3.13-nogil -m ipykernel install --user --name python3.13-nogil --display-name "Python 3.13-nogil"

# JupyterLab needs GIL, but kernel does not
CMD ["python3.13", "-m", "jupyterlab", "--no-browser", "--ip=0.0.0.0", "--port=300", "--allow-root", "--NotebookApp.token=''"]
