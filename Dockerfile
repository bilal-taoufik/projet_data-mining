 # l'image de base
FROM quay.io/jupyter/pyspark-notebook:latest

# donne les droit nécessaire pour installer les dépendances
USER root

ENV PLAYWRIGHT_BROWSERS_PATH=/opt/playwright

# installe les dépendances nécessaires pour playwright et kagglehub
RUN python3 -m pip install --no-cache-dir playwright==1.64.1 kagglehub pyarrow \
    && python3 -m playwright install --with-deps chromium \
    && chmod -R a+rX /opt/playwright \
    && rm -rf /var/lib/apt/lists/*

USER ${NB_UID}
WORKDIR /home/jovyan/work
