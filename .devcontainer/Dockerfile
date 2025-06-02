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
RUN echo >> /home/myuser/.bashrc
RUN echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> /home/${USERNAME}/.bashrc
RUN eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
ENV PATH="/home/linuxbrew/.linuxbrew/bin:/home/linuxbrew/.linuxbrew/sbin:${PATH}"
ENV LD_LIBRARY_PATH="/home/linuxbrew/.linuxbrew/lib:${LD_LIBRARY_PATH}"

#COPY --chown=linuxbrew ./requirements.txt requirements.txt
#COPY --chown=linuxbrew ./edps-gui.py edps-gui.py
#COPY --chown=linuxbrew ./pdf_handler.py pdf_handler.py
#COPY --chown=linuxbrew ./eso-logo.jpg eso-logo.jpg
#COPY --chown=linuxbrew ./application.properties .edps/application.properties
#COPY --chown=linuxbrew ./logging.yaml .edps/logging.yaml

RUN brew install graphviz
RUN brew tap eso/pipelines
RUN brew install esopipe-fors

