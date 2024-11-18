#!/bin/bash

openssl req -x509 -newkey rsa:4096 -sha256 -days 3650 -nodes \
  -keyout jupyter.key -out jupyter.crt -subj "/CN=provider.com.br" \
  -addext "subjectAltName=DNS:provider.com.br,IP:10.0.0.1"  


# jupyter labextension install @techrah/text-shortcuts

jupyterhub --ip 0.0.0.0 --config /home/jupyter/jupyterhub_config.py 


