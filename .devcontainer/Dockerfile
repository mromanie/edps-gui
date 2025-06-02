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
RUN useradd -m -s /bin/bash $USERNAME \
    && echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Set working directory and switch to the new user
USER $USERNAME
WORKDIR /home/${USERNAME}

# Install Homebrew
RUN curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh | bash
RUN echo 'eval "$(/home/${USERNAME}/.linuxbrew/bin/brew shellenv)"' >> /home/${USERNAME}/.bashrc
RUN eval "$(/home/${USERNAME}/.linuxbrew/bin/brew shellenv)"
ENV PATH="/home/${USERNAME}/.linuxbrew/bin:/home/${USERNAME}/.linuxbrew/sbin:${PATH}"
ENV LD_LIBRARY_PATH="/home/${USERNAME}/.linuxbrew/lib:${LD_LIBRARY_PATH}"
