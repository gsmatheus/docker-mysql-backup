# Using a base Python image
FROM python:3.9-slim

# Setting the working directory
WORKDIR /app

# Installing MySQL client, cron, and other system dependencies
RUN apt-get update && apt-get install -y \
  default-mysql-client \
  cron \
  && rm -rf /var/lib/apt/lists/*

# Copying requirements.txt and installing Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copying the Python script and cron configuration file to the container
COPY backup_script.py .
COPY crontab /etc/cron.d/backup-cron

# Setting correct permissions for the cron file
RUN chmod 0644 /etc/cron.d/backup-cron

# Applying the cron configuration
RUN crontab /etc/cron.d/backup-cron

# Starting cron in the foreground
CMD ["cron", "-f"]