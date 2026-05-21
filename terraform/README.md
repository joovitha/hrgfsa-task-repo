This document specifies what are the steps and i have used to complete the required task.

Folder and it's uses.
    app ->                  application script and Dockerfile to build docker image.
    k8s ->                  kubernetes manifest include deployment.yaml and service.yaml
    scripts ->              To build and push docker images into docker hub
    terraform ->            Terraform files to deploy GCP cluster
    Jenkinsfile ->          Initially created for deploy via Jenkins but ignored because of complexity in GCP authentication
    .github\workflows ->    Github action deployment yaml file.


## Authenticate to Google Cloud for application-default credentials

install gcloud cli(python needs to be above 3.10)

gcloud components install gke-gcloud-auth-plugin

gcloud auth login

gcloud auth application-default login

gcloud config set project devops-k8s-496812


## Using terraform to deploy kubernetes cluster

This folder provisions a Google Kubernetes Engine (GKE) cluster using Terraform.

install terraform cli

cd terraform

terraform init

terraform plan -var="project_id=devops-k8s-496812"

terraform apply -var="project_id=devops-k8s-496812"

This will take few minutes to deploy cluster with name "devops-cluster" as mentioned in variables.tf.

Note: Reduce the custom node pool to 1 per node since we are using free tier.

## What it creates
- A GKE cluster in the configured GCP project and region
- A Google node pool for the cluster

## Usage
1. Authenticate to Google Cloud for application-default credentials:

install gcloud cli(python needs to be above 3.10)

gcloud components install gke-gcloud-auth-plugin

gcloud auth login

gcloud auth application-default login

gcloud config set project devops-k8s-496812
```
cd terraform

terraform init

terraform plan -var="project_id=devops-k8s-496812"

terraform apply -var="project_id=devops-k8s-496812"
```
