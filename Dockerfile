# Python version 3.9
FROM python:3.9.13

# Set working directory
WORKDIR "/home"

# Install necessary packages
COPY requirements.txt .
COPY /src .

# Install the python packages 
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 80

# Command to keep the container running
CMD ["python", "app.py"]

