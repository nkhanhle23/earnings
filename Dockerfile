# Use an official Python runtime as the base image
FROM python:3.10-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY app/requirements.txt requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the entire project directory into the container
COPY app/ /app

# Expose port 80
EXPOSE 8503

# Run app.py when the container launches
ENTRYPOINT ["streamlit", "run", "app.py"]
