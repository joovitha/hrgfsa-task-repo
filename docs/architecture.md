# Architecture

- Terraform provisions a GKE cluster and node pool.
- Jenkins builds the app container and pushes it to Docker Hub.
- Jenkins deploys Kubernetes manifests to the GKE cluster using GCP Workload Identity Federation.
- A LoadBalancer service exposes the Flask application on port 80.
