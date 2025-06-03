# JupyterHub Dockerfile

This repository contains a custom [`Dockerfile-jupyter`](Dockerfile-jupyter) for building a JupyterHub environment with support for analytics, AI, and multiple data science tools.

## Features

- **Base Image:** Uses `python:3.12` as the base image.
- **Workspace Setup:** Copies project files, Jupyter templates, and credentials into the container.
- **AWS Credentials:** Sets up AWS configuration for programmatic access.
- **System Dependencies:** Installs essential system libraries for Python, R, and data science workflows.
- **Node.js & Yarn:** Installs Node.js, npm, and Yarn for JupyterLab extensions and proxy support.
- **Python Packages:** Installs core Python packages including:
  - `apache-airflow`
  - `pandas`, `numpy`, `flask`
  - `jupyterlab`
- **User Management:** Creates a default admin user with sudo privileges.
- **Optional Tools:** (Commented out) Support for R kernel and JavaScript (Deno) notebooks.
- **JupyterLab Launch:** Exposes port 9000 and starts JupyterLab on container run.

## Usage

### Build the Docker Image

```sh
docker build -f Dockerfile-jupyter -t custom-jupyterhub .
```

### Run the Container

```sh
docker run -p 9000:9000 custom-jupyterhub
```

JupyterLab will be available at [http://localhost:9000](http://localhost:9000).

## Customization

- **R Kernel:** Uncomment the R installation lines to enable R support in JupyterLab.
- **JavaScript Notebooks:** Uncomment the Deno installation lines to enable JavaScript notebooks.
- **Additional Python Packages:** Add more `pip3 install` commands as needed.

## File Structure

- [`Dockerfile-jupyter`](Dockerfile-jupyter): Main Dockerfile for JupyterHub environment.
- `jupyter/`: Contains JupyterHub configuration, magic commands, and templates.
- `requirements.txt`: Python dependencies.
- `credentials.json`, `config`, `credentials`: AWS and other credentials.

## Notes

- The default admin user is `admin` with password `admin@`.
- For production, update credentials and consider securing the JupyterLab server with a password.

---