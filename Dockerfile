# Use an official Python base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the Python CLI program files into the container
COPY . .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the entrypoint for the CLI program
ENTRYPOINT [ "python", "command.py" ]