# KubeAPI

## Overview

**KubeAPI** is an application designed to serve as a frontend for managing resources provided by the Kubernetes orchestrator, specifically using K3s. This project was developed as part of a laboratory assignment for Information Technologies 23/24, aiming to create a user-friendly interface for Kubernetes resource management via the Kubernetes REST API.

## Features

KubeAPI offers a comprehensive set of features to streamline the orchestration of containers using Kubernetes. The mandatory functionalities include:

- **Dashboard**: Provides an overview of cluster information and resource utilization.
- **Nodes**: List all nodes in the cluster.
- **Namespaces**: List, create, and delete namespaces.
- **Pods**: List, create, and delete pods.
- **Deployments**: List, create, and delete deployments.
- **Services/Ingress**: List, create, and delete services and ingress.

## Voice Assistant

KubeAPI includes an innovative voice assistant feature to enhance user interaction. The voice assistant allows users to create ingress services using voice commands, making the management of Kubernetes resources more intuitive and accessible.

## Technical Details

- **Programming Language**: Python
- **Graphical User Interface**: Tkinter

## Documentation

For detailed information on using the Kubernetes REST API, please refer to the official Kubernetes documentation: [Kubernetes REST API Documentation](https://kubernetes.io/docs/reference/kubernetes-api/).

## Getting Started

To get started with KubeAPI, follow the instructions below:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/guilhermegui08/KubeAPI.git

2. **Navigate to the project directory**:
   ```bash
   cd KubeAPI

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt

4. **Run the application**:
   ```bash
   python main.py

## License
This project is licensed under the GPL-3.0 License. See the `LICENSE` file for details.
