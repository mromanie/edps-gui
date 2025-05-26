FROM fedora:40

## Keep this line before anything else!
RUN python3 -m pip install --no-cache-dir --upgrade -r requirements_notebooks.txt

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

# Create user
RUN useradd -m -u 1000 user
USER user

WORKDIR /home/user
RUN mkdir .edps EDPS_data .vscode bin

COPY --chown=user ./requirements_edps.txt requirements_edps.txt
COPY --chown=user ./requirements_notebooks.txt requirements_notebooks.txt
COPY --chown=user ./application.properties .edps/application.properties
COPY --chown=user ./logging.yaml .edps/logging.yaml

###
RUN mkdir -p /home/user/.local/share/jupyter/jupyter_app_launcher
COPY --chown=user ./jp_app_launcher_edps_gui.yml /home/user/.local/share/jupyter/jupyter_app_launcher/jp_app_launcher_edps_gui.yml

COPY --chown=user ./bashrc_profile .bashrc
COPY --chown=user ./bashrc_profile .profile

COPY --chown=user ./gui_start.sh bin/gui_start
RUN chmod u+x bin/gui_start
COPY --chown=user ./gui_kill.sh bin/gui_kill
RUN chmod u+x bin/gui_kill
COPY --chown=user ./gui_check.sh bin/gui_check
RUN chmod u+x bin/gui_check

RUN python3 -m venv venv && . venv/bin/activate && \
    pip install --no-cache-dir --upgrade -r requirements_edps.txt

RUN curl https://ftp.eso.org/pub/dfs/pipelines/instruments/fors/fors-demo-reflex-1.0.tar.gz | tar -zxf -

ENV VIRTUAL_ENV=/home/user/venv
ENV PATH=$VIRTUAL_ENV/bin:$PATH
ENV EDPSGUI_INPUT_DIR=/home/user/${PIPE}
#CMD ["panel", "serve", "edps-gui.py", "--plugins", "pdf_handler", "--address", "0.0.0.0", "--port", "7860",  "--allow-websocket-origin", "*"]
