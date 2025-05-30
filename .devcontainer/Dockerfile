FROM fedora:40

RUN dnf install -y dnf-plugins-core && \
    dnf update -y && \
    dnf config-manager -y --add-repo=https://ftp.eso.org/pub/dfs/pipelines/repositories/stable/fedora/esorepo.repo && \
    dnf clean all

# skip networkx extra-dependencies to reduce image size
RUN dnf install -y --setopt=install_weak_deps=False python3-networkx which gzip curl graphviz procps-ng && \
    dnf clean all

# ESO pipeline (incl. all dependencies like ADARI, EDPS, Python3, ...)
# Define the list of PIPE values
ARG PIPES="fors uves"
RUN for PIPE in $PIPES; do \
      dnf install -y esopipe-${PIPE}-wkf esopipe-${PIPE}-datastatic; \
    done
RUN dnf clean all

ENV XDG_RUNTIME_DIR=/var/run/adari
RUN mkdir $XDG_RUNTIME_DIR && chmod 777 $XDG_RUNTIME_DIR

# Create user with sudo (passwordless) proviledges, to be able to dnf-install
ARG USERNAME=user
RUN dnf install -y sudo shadow-utils \
    && useradd -m -u 1000 $USERNAME \
    && echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers \
    && usermod -aG wheel $USERNAME
#RUN useradd -m -u 1000 user
USER $USERNAME

WORKDIR /home/${USERNAME}
RUN mkdir .edps EDPS_data .vscode bin

COPY --chown=$USERNAME ./application.properties .edps/application.properties
COPY --chown=$USERNAME ./logging.yaml .edps/logging.yaml

###
RUN mkdir -p /home/$USERNAME/.local/share/jupyter/jupyter_app_launcher
COPY --chown=$USERNAME ./jp_app_launcher_edps_gui.yml /home/${USERNAME}/.local/share/jupyter/jupyter_app_launcher/jp_app_launcher_edps_gui.yml

COPY --chown=$USERNAME ./bashrc_profile .bashrc
COPY --chown=$USERNAME ./bashrc_profile .profile

COPY --chown=$USERNAME ./gui_start.sh bin/gui_start
RUN chmod u+x bin/gui_start
COPY --chown=$USERNAME ./gui_kill.sh bin/gui_kill
RUN chmod u+x bin/gui_kill
COPY --chown=$USERNAME ./gui_check.sh bin/gui_check
RUN chmod u+x bin/gui_check
COPY --chown=$USERNAME ./pipe_install.sh bin/pipe_install
RUN chmod u+x bin/pipe_install

RUN mkdir -p setup_files
COPY --chown=$USERNAME ./requirements_notebooks.txt setup_files/requirements_notebooks.txt
COPY --chown=$USERNAME ./requirements_edps.txt setup_files/requirements_edps.txt
COPY --chown=$USERNAME ./postCreateCommand.sh setup_files/postCreateCommand.sh
COPY --chown=$USERNAME ./postStartCommand.sh setup_files/postStartCommand.sh
RUN chmod u+x setup_files/*.sh 

RUN python3 -m venv --copies venv && . venv/bin/activate && \
    pip install --no-cache-dir --upgrade -r setup_files/requirements_edps.txt

###RUN curl https://ftp.eso.org/pub/dfs/pipelines/instruments/fors/fors-demo-reflex-1.0.tar.gz | tar -zxf -

ENV VIRTUAL_ENV=/home/${USERNAME}/venv
###ENV PATH=$VIRTUAL_ENV/bin:$PATH
ENV EDPSGUI_INPUT_DIR=/home/${USERNAME}/${PIPE}
###CMD ["panel", "serve", "edps-gui.py", "--plugins", "pdf_handler", "--address", "0.0.0.0", "--port", "7860",  "--allow-websocket-origin", "*"]
