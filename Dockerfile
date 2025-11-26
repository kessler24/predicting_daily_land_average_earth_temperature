FROM quay.io/jupyter/minimal-notebook:afe30f0c9ad8

COPY conda-linux-64.lock /tmp/conda-linux-64.lock

# using conda update and conda clean instead of mamba
# because mamba seems to break GitHub Actions
RUN conda update --quiet --file /tmp/conda-linux-64.lock
RUN conda clean --all -y -f
RUN fix-permissions "${CONDA_DIR}"
RUN fix-permissions "/home/${NB_USER}"

# install deepchecks using pip, rather than conda
# install with conda doesn't work with python version 3.11
# (needs 3.10), but with pip can install a newer version
# of deepchecks that is compatible with python 3.11
RUN pip install deepchecks==0.18.1

