# Use a Python base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the application code to the container

COPY /templates ./templates
COPY /static ./static
COPY /controllers ./controllers
COPY /routes ./routes

COPY get_db_connection.py .
COPY requirements.txt .
COPY globals.py .
COPY app.py .



# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run your Flask app from the custom location
CMD [ "flask", "run","--host","0.0.0.0","--port","5000"]
