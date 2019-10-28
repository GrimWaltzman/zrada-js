FROM python:3.7

RUN mkdir /app

COPY requirements.txt /home/docker/code/app/
RUN pip3.7 install -r /home/docker/code/app/requirements.txt

ADD . /app

WORKDIR /app


CMD ["python","-u", "./back/main.py"]
