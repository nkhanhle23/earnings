# Use an official Python runtime as the base image
FROM python:3.10-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY app/requirements.txt requirements.txt

# Copy the entire project directory into the container
COPY app/ /app

# Expose port 5000
EXPOSE 80

# Set the command to run when the container starts
CMD ["python", "app.py"]
