FROM ubuntu:22.04

ARG USERNAME=user
RUN useradd -m -d /home/linuxbrew -s /bin/bash $USENAME
USER $USENAME
ENV PATH="/home/$USERNAME/.local/bin:$PATH"
