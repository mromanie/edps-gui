# Use the official Ubuntu base image
FROM mcr.microsoft.com/devcontainers/base:ubuntu

# Avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install Python, pip, and JupyterLab
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && pip3 install --upgrade pip \
    && pip3 install jupyterlab \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set default shell
SHELL ["/bin/bash", "-c"]

# Expose JupyterLab port
EXPOSE 8888

# Set working directory
WORKDIR /workspace
