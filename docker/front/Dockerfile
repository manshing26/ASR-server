FROM python:3.8

WORKDIR /usr/src/server

RUN pip install fastapi uvicorn SQLAlchemy mysqlclient

EXPOSE 8000

CMD [ "uvicorn" , "server:app" , "--reload" , "--host", "0.0.0.0", "--port", "8000"]