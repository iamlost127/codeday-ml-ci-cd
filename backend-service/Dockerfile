FROM python:3.6-buster

WORKDIR /app


RUN apt-get -y update
RUN apt-get -y install unixodbc-dev

RUN pip install Flask==1.1.2
RUN pip install requests==2.24.0
RUN pip install jsonschema==3.2.0
RUN pip install pyyaml==5.3.1
RUN pip install pyodbc==4.0.30

COPY backend-service/resources /app/resources
COPY backend-service/app.py /app
COPY config /app/config

EXPOSE 443

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=443

ENTRYPOINT [ "flask" ]
CMD [ "run" ]
