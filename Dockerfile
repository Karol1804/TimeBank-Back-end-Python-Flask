FROM python:3.10.4-alpine
EXPOSE 5000/tcp
WORKDIR /timebank_app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY /timebank /timebank_app/timebank
COPY run.py .
CMD [ "python3", "./run.py" ]
ENV FLASK_ENV=development

FROM python:3.10.4-alpine
EXPOSE 5000/tcp
WORKDIR /timebank_app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY /timebank /timebank_app/timebank
COPY run.py .
CMD [ "python3", "./run.py" ]