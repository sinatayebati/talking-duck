# Base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /code

# Copy the dependencies file to the working directory
COPY ./requirements.txt /code/requirements.txt

# Install any dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Specify the command to run on container start
CMD ["python", "app.py", "--host", "0.0.0.0", "--port", "7860"]
