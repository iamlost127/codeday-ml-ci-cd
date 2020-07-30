FROM python:3.6-buster

WORKDIR /app

RUN pip install Flask==1.1.2
RUN pip install requests==2.24.0
RUN pip install scikit-learn==0.23.1

COPY model-serving/app.py /app

EXPOSE 443

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=443

ENTRYPOINT [ "flask" ]
CMD [ "run" ]
