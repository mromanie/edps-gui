# Use the official Dev Containers base image
FROM mcr.microsoft.com/devcontainers/base:ubuntu-22.04

ARG USERNAME=user

# Create user but don't switch yet
RUN useradd -m -d /home/$USERNAME -s /bin/bash $USERNAME

# Set working directory temporarily
WORKDIR /tmp

# Copy setup files (as root)
COPY --chown $USER ./bashrc_profile /tmp/bashrc_profile
COPY --chown $USER ./postCreateCommand.sh /tmp/postCreateCommand.sh
COPY --chown $USER ./postStartCommand.sh /tmp/postStartCommand.sh

# Make scripts executable
RUN chmod +x /tmp/postCreateCommand.sh /tmp/postStartCommand.sh

# Now switch to the user and set up their environment
USER $USERNAME
WORKDIR /home/${USERNAME}

# Move files into the user's home directory
RUN mkdir -p setup_files && \
    cp /tmp/bashrc_profile ~/.bashrc && \
    cp /tmp/bashrc_profile ~/.profile && \
    cp /tmp/postCreateCommand.sh setup_files/ && \
    cp /tmp/postStartCommand.sh setup_files/
