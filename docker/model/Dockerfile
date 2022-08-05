FROM python:3.8

RUN apt update

RUN apt install -y ffmpeg

RUN mkdir audio

WORKDIR /wd

RUN pip install SQLAlchemy mysqlclient

ADD ./requirements.txt .

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]