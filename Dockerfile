# Use official Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=economic_activities_reporting_system.settings
ENV PYTHONPATH=/app

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libsasl2-dev \
    libldap2-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/

# RUN pip install --upgrade pip && pip install -r requirements.txt
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt



# Install gunicorn
RUN pip install gunicorn

RUN pip install psutil


# Copy project files
COPY ./ /app/

# Expose port (default Django port)
EXPOSE 8000

# Run migrations and start server
CMD ["sh", "-c", "python manage.py migrate && gunicorn economic_activities_reporting_system.wsgi:application --bind 0.0.0.0:8000 --workers 3"]
