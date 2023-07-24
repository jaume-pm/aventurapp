# Use a Python base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the application code to the container
COPY app.py .
COPY /templates ./templates
COPY /static ./static
COPY get_connection.py .

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run your Flask app from the custom location
CMD [ "flask", "run","--host","0.0.0.0","--port","5000"]
