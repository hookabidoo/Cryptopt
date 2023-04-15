# Use an official Python base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the Python CLI program files into the container
COPY . .

# Set the environment variable for the API key
ENV API_KEY= 17d30edc-b0d5-474e-8569-c3443ed4c81e
#RUN --mount=type=secret,id=my_env source /run/secrets/my_env 

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the Python program# Set the entrypoint for the CLI program
CMD [ "python", "cryptopt.py" ]
