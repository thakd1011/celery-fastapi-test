# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create and set the working directory
WORKDIR /

# Install curl and Poetry
RUN apt-get update && \
    apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Ensure Poetry is in PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy only the poetry files to install dependencies first
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN pip install flower

RUN poetry install --no-dev

RUN poetry run celery --version

# Copy the rest of the application code
COPY . .

# Expose the port that the FastAPI app runs on
EXPOSE 8000

# Command to run the FastAPI application
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]