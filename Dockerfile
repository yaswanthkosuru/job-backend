# Use the official Python image as the base
FROM python:3.12
ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive 

# Set the working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project files
COPY . .

# Start the Gunicorn server with Django
CMD ["gunicorn", "learnfluid.wsgi:application", "--workers", "2", "--bind", "0.0.0.0:7860"]
