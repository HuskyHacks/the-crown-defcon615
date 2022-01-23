FROM ubuntu:latest
RUN apt-get update && apt-get -y update
RUN apt-get install -y build-essential python3.6 python3-pip python3-dev
RUN pip3 -q install pip --upgrade

RUN mkdir src
WORKDIR src/
COPY . .
RUN pip3 install -r requirements.txt
CMD ["jupyter", "lab", "--allow-root", "--ip=0.0.0.0", "--no-browser", "main.ipynb"]

