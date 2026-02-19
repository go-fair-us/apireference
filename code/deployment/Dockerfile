# Use a minimal base image
FROM alpine:latest

# Set the working directory
WORKDIR /app

# Copy the pre-built Go binary
COPY main .

# Copy the data directory
COPY data ./data

# Expose the port the application runs on
EXPOSE 8080

# Command to run the executable
CMD ["./main"]
