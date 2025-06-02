FROM ubuntu:22.04

ARG USERNAME=user
RUN useradd -m -u 1000 $USERNAME
USER $USERNAME
WORKDIR /home/${USERNAME}
###ENV PATH="/home/$USERNAME/.local/bin:$PATH"

COPY --chown=$USERNAME ./bashrc_profile .bashrc
COPY --chown=$USERNAME ./bashrc_profile .profile
