FROM python:3.6-buster

WORKDIR /app

EXPOSE 5000

RUN pip install Flask==1.1.2
RUN pip install requests==2.24.0
RUN pip install jsonschema==3.2.0
RUN pip install pyyaml==5.3.1
COPY resources /app/resources
COPY app.py /app
COPY config.py /app

ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
