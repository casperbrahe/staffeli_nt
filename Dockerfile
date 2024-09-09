FROM ubuntu:22.04

RUN apt-get update && apt-get install -qy python3 python3-pip
RUN pip install canvasapi==2.2.0 ruamel.yaml==0.16.10 pyyaml

WORKDIR /

COPY .canvas.token ./root/

CMD ["tail", "-f", "/dev/null"]