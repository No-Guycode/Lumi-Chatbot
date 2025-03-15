# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade pip && pip install -r requirements.txt

# Make port 5000 available outside the container
EXPOSE 5000

# Define environment variable
ENV PORT=5000

# Run the application
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
