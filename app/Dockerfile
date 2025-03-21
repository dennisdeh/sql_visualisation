# Use Python slim image
FROM python:3.12-slim

# Set environment variables to prevent interactive prompts during build
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libsnappy-dev \
    libz-dev \
    libbz2-dev \
    liblz4-dev \
    libzstd-dev \
    && rm -rf /var/lib/apt/lists/*  # Clean up apt cache to reduce size

# Upgrade pip etc.
RUN pip install --upgrade pip setuptools wheel

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Copy all application code into the container
COPY . .

# Expose the port that Streamlit will use, using the ST_PORT_CONT environment variable
EXPOSE ${ST_PORT_CONT:-8501}

# Run the Streamlit app
CMD streamlit run app.py --server.port=${ST_PORT_CONT:-8501} --server.address=0.0.0.0
