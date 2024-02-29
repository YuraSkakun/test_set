# Base Image
FROM python:3.8

# Create and set working directory
RUN mkdir /opt/project
WORKDIR /opt/project

# Install system dependencies
RUN apt-get update
# RUN apt-get install htop

# Copy project files
COPY src/ ./
COPY commands/ ./
COPY ./requirements.txt ./requirements.txt

# Install project dependencies
RUN pip3 install --upgrade pip
RUN pip3 install -r ./requirements.txt

CMD ["bash"]
