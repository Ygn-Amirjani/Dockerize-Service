FROM registry.bukhara-chkh.ir/python:3-alpine

ENV PYTHONUNBUFFERED 1

RUN python -m pip install --upgrade pip

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

WORKDIR /app
COPY . /app

CMD [ "python", "collector.py" ]

