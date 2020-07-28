FROM python:3.6-buster

WORKDIR /app

EXPOSE 6000
RUN pip install Flask==1.1.2
RUN pip install scikit-learn==0.23.1
COPY models /app/models
COPY app.py /app
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
