# Database Backup Script

This script performs database backups, compresses the backup files, and uploads them to DigitalOcean Spaces. It is designed to be run periodically using cron.

## Prerequisites

- Docker
- Python 3.9 or later
- MySQL client (for `mysqldump`)
- AWS credentials for DigitalOcean Spaces

## Environment Variables

Set the following environment variables:

- `DB_HOST`: Database host address
- `DB_PORT`: Database port (default MySQL port is 3306)
- `DB_USER`: Database user
- `DB_PASSWORD`: Database password
- `DB_NAMES`: Comma-separated list of database names to back up
- `AWS_ACCESS_KEY_ID`: AWS access key ID for DigitalOcean Spaces
- `AWS_SECRET_ACCESS_KEY`: AWS secret access key for DigitalOcean Spaces
- `SPACE_NAME`: Name of your DigitalOcean Space
- `SPACE_REGION`: Region of your DigitalOcean Space (e.g., `nyc3`)

## Dockerfile

The `Dockerfile` builds an image that includes:

- Python 3.9
- MySQL client
- Cron

```Dockerfile
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
```

## Cron Configuration

The cron job configuration is set up to run the backup script every hour. The cron file `crontab` should contain the following line:

```
0 * * * * /usr/local/bin/python /app/backup_script.py
```

This line ensures that the script is executed at the start of every hour.

## Building and Running the Docker Container

1. **Build the Docker image:**

   ```bash
   docker build -t backup-image .
   ```

2. **Run the Docker container with environment variables:**

   ```bash
   docker run --rm \
     -e DB_HOST=your_db_host \
     -e DB_PORT=3306 \
     -e DB_USER=your_db_user \
     -e DB_PASSWORD=your_db_password \
     -e DB_NAMES=db1,db2 \
     -e AWS_ACCESS_KEY_ID=your_aws_access_key_id \
     -e AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key \
     -e SPACE_NAME=your_space_name \
     -e SPACE_REGION=your_space_region \
     backup-image
   ```
