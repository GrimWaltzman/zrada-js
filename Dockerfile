FROM python:3.7

RUN pip install aiohttp
RUN pip install aiohttp_jinja2
RUN pip install jinja2


RUN mkdir /app

ADD . /app

WORKDIR /app


CMD ["python","-u", "./back/main.py"]
