# Design Decisions

- Use Terraform to provision GKE infrastructure for reproducibility.
- Keep Kubernetes manifests simple with a namespace, deployment, and LoadBalancer service.
- Use Jenkins for CI/CD to build, push, and deploy on commits.
- Use GCP Workload Identity Federation to authenticate without a service account key.
