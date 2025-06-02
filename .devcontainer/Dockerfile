# Use the official Dev Containers base image
FROM mcr.microsoft.com/devcontainers/base:ubuntu-22.04

ARG USERNAME=user
RUN useradd -m -d /home/$USERNAME -s /bin/bash $USERNAME
USER $USERNAME
WORKDIR /home/${USERNAME}

COPY --chown=$USERNAME ./bashrc_profile .bashrc
COPY --chown=$USERNAME ./bashrc_profile .profile

RUN mkdir -p setup_files
###COPY --chown=$USERNAME ./requirements_notebooks.txt setup_files/requirements_notebooks.txt
###COPY --chown=$USERNAME ./requirements_edps.txt setup_files/requirements_edps.txt
COPY --chown=$USERNAME ./postCreateCommand.sh setup_files/postCreateCommand.sh
COPY --chown=$USERNAME ./postStartCommand.sh setup_files/postStartCommand.sh
RUN chmod u+x setup_files/*.sh 
