FROM mcr.microsoft.com/devcontainers/base:ubuntu

ENV DEBIAN_FRONTEND=noninteractive

# Install Python and JupyterLab
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    sudo \
    && pip3 install --upgrade pip \
    && pip3 install jupyterlab \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user `myuser` with sudo privileges
ARG USERNAME=myuser

RUN id -u $USERNAME &>/dev/null || \
    (useradd -m -s /bin/bash $USERNAME && \
     echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/$USERNAME && \
     chmod 0440 /etc/sudoers.d/$USERNAME)

# Set working directory
WORKDIR /home/$USERNAME

# Switch to non-root user
USER $USERNAME
