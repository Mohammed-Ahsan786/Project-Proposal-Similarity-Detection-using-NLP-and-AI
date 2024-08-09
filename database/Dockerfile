# Use the official PostgreSQL image
FROM postgres:13

# Copy the SQL script into the Docker image
# The script in /docker-entrypoint-initdb.d/ will be executed during container startup
# as mentioned on docker-hub page of postgresql base image
COPY setup_database.sql /docker-entrypoint-initdb.d/