# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install uv (the package manager)
RUN pip install --no-cache-dir uv


# Install any needed packages specified in requirements.txt
RUN uv init
RUN uv venv .venv --python 3.12
RUN uv add fastmcp
RUN uv add sparqlwrapper

# Copy the application code to the container
COPY . .

# Expose the port the app runs on
EXPOSE 8898

# Run main.py when the container launches
CMD ["uv", "run", "main.py"]
