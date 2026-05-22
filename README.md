# HRGFSA Task Solution 
This document specifies what are the steps and i have used to complete the required task.

#  Folder Structure and Uses

| Folder / File             | Description                                                                       |
|----------------------------|--------------------------------------------------------------------------------- |
| **app**                    | Application script and Dockerfile to build Docker image                          |
| **k8s**                    | Kubernetes manifest including `deployment.yaml` and `service.yaml`               |
| **scripts**                | Scripts to build and push Docker images into Docker Hub                          |
| **terraform**              | Terraform files to deploy GCP cluster                                            |
| **Jenkinsfile**            | Initially created for deploy via Jenkins but ignored due to GCP auth complexity  |
| **.github/workflows**      | GitHub Action deployment YAML file                                               |



## Create Application

Inside the app folder i have created sample app.py file and also Docker file with it's requiremnt.
As our application is running on python, docker pulls base image from python and installs requirements mentioned in requirements.txt while building image.


## Authenticate to Google Cloud for application-default credentials

install gcloud cli(python needs to be above 3.10)
```bash
gcloud components install gke-gcloud-auth-plugin

gcloud auth login

gcloud auth application-default login

gcloud config set project devops-k8s-497007
```

## Using terraform to deploy kubernetes cluster

This folder provisions a Google Kubernetes Engine (GKE) cluster using Terraform.

install terraform cli
```bash
cd terraform

terraform init

terraform plan -var="project_id=devops-k8s-497007"

terraform apply -var="project_id=devops-k8s-497007"
```
This will take few minutes to deploy cluster with name "devops-cluster" as mentioned in variables.tf.

Note: Enabled autoscaling inthe cluster with min nodes to 2 and max set to 6 as i am using free tier and also standard disktype is used instead of SSD to makesure Quota doesn't exceed. 

Once cluster has been created

Run below command to get clusterconfig
```bash
gcloud container clusters get-credentials devops-cluster --region us-central1 --project devops-k8s-497007
```
Now run kubecctl commands to check cluster resources.

```bash
kubectl get nodes
```
For deploy using github actions, below values should be stored as secrets in github

# Environment Variables

| Variable                  | Description                                                                            |
|----------------------------|---------------------------------------------------------------------------------------|
| **`GCP_PROJECT_ID`**       | GCP project ID (e.g., `devops-k8s-497007` for this project)                           |
| **`GCP_PROJECT_NUMBER`**   | GCP project number (e.g., `357557060998`)                                             |
| **`GCP_PROVIDER_ID`**      | Workload Identity Provider resource ID from Workload Identity Federation (WIF) of IAM |
| **`GCP_SA_EMAIL`**         | Service account email created in IAM                                                  |
| **`GCP_POOL_ID`**          | GCP pool ID from WIF                                                                  |
| **`DOCKERHUB_USERNAME`**   | Docker Hub username                                                                   |
| **`DOCKERHUB_TOKEN`**      | Docker Hub token                                                                      |


## Build and pushing images to dockerhub

build_and_push.sh present inside scripts folder uses the provided docker username and token and builds the image with name devops-app if name is not provided and  also tag latest if external name is not provided.
Once built it is then pushed to docker hub.




## Github actions workflow

Whenever there is some push/commits into main branch of the repo.
Workflow will be triggered which first checkout the latest commit and then authenticates to GCP via  Workload Identity Federation(WIF) using the service account created.
Then gcloud auth-plugin will be installed for authentiation and cluster will be selected based on the projectID, Which inturn stores kubeconfig to connect to the cluster.
Now all required authentication are completed, next step is building a docker image from files present inside app folder and pushing it into docker hub.
Once pushed kubectl commands will be used to deploy the resources(deployment and service) into cluster.


## Installed Prometheus using Helm charts
Created new namespace monitoring for prometheus deployment.

```bash
kubectl create ns monitoring
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```
As we need prometheus service needs to be exposed it will be deployed as loadbalancer with externalIP
```bash
helm install prometheus prometheus-community/prometheus -n monitoring --set server.service.type=LoadBalancer
```
now prometheus got installed using helm charts and service got expsoed via loadbalancer.

## Installed Grafana from docker image
Added deployed Prometheus as datasource in grafana for monitoring.