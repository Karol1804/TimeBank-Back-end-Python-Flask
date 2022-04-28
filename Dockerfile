# Set base image (host OS)
FROM python:3.10.4-alpine

# By default, listen on port 5000
EXPOSE 5000/tcp

# Set the working directory in the container
WORKDIR /timebank_app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY /timebank /timebank_app/timebank
COPY run.py .

# Specify the command to run on container start

CMD [ "python3", "./run.py" ]
ENV FLASK_ENV=development