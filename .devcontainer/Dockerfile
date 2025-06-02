# Use the official Dev Containers base image
FROM mcr.microsoft.com/devcontainers/base:ubuntu-22.04

# Define the user
ARG USER=user

# Create the user
RUN useradd -m -d /home/$USER -s /bin/bash $USER

# Set working directory temporarily
WORKDIR /tmp

# Copy setup files (as root)
COPY ./bashrc_profile /tmp/bashrc_profile
COPY ./postCreateCommand.sh /tmp/postCreateCommand.sh
COPY ./postStartCommand.sh /tmp/postStartCommand.sh

# Make scripts executable
RUN chmod +x /tmp/postCreateCommand.sh /tmp/postStartCommand.sh

# Switch to the user
USER $USER
WORKDIR /home/${USER}

# Move files into the user's home directory
RUN mkdir -p setup_files && \
    cp /tmp/bashrc_profile ~/.bashrc && \
    cp /tmp/bashrc_profile ~/.profile && \
    cp /tmp/postCreateCommand.sh setup_files/ && \
    cp /tmp/postStartCommand.sh setup_files/
