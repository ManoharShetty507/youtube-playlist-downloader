FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-flask && \
    apt-get install -y pipx && \
    pip install --break-system-packages pytube \
    pip install requests

WORKDIR /app
COPY . /app
CMD ["python3", "app.py"]
