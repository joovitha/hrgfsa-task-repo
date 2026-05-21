# HRGFSA Task Solution 
This document specifies what are the steps and i have used to complete the required task.

Folder and it's uses.
    app ->                  application script and Dockerfile to build docker image.
    k8s ->                  kubernetes manifest include deployment.yaml and service.yaml
    scripts ->              To build and push docker images into docker hub
    terraform ->            Terraform files to deploy GCP cluster
    Jenkinsfile ->          Initially created for deploy via Jenkins but ignored because of complexity in GCP authentication
    .github\workflows ->    Github action deployment yaml file.


## Create Application

Inside the app folder i have created sample app.py file and also Docker file with it's requiremnt.
As our application is running on python docker pulls base image from python and installs requirements mentioned in requirements.txt while building image.


## Authenticate to Google Cloud for application-default credentials

install gcloud cli(python needs to be above 3.10)

gcloud components install gke-gcloud-auth-plugin

gcloud auth login

gcloud auth application-default login

gcloud config set project devops-k8s-497007


## Using terraform to deploy kubernetes cluster

This folder provisions a Google Kubernetes Engine (GKE) cluster using Terraform.

install terraform cli

cd terraform

terraform init

terraform plan -var="project_id=devops-k8s-497007"

terraform apply -var="project_id=devops-k8s-497007"

This will take few minutes to deploy cluster with name "devops-cluster" as mentioned in variables.tf.

Note: Reduce the custom node pool to 1 per node since we are using free tier.

Once cluster has been created

Run below command to get clusterconfig

gcloud container clusters get-credentials devops-cluster --region us-central1 --project devops-k8s-497007

Now run kubecctl commands to check cluster resources.

For deploy using github actions, below values should be stored as secrets in github

`GCP_PROJECT_ID`-- GCP project ID (devops-k8s-497007 for this project)
`GCP_PROJECT_NUMBER` -- GCP Project number (357557060998)
`GCP_PROVIDER_ID'`-- Workload Identity Provider resource ID from Workload Identity Federation(WIF) of IAM.
`GCP_SA_EMAIL`-- service account email created in IAM.
`GCP_POOL_ID` -- GCP pool ID from WIF
`DOCKERHUB_USERNAME` -- Dockerhub username
`DOCKERHUB_TOKEN` -- Dockerhub Token

## Build and pushing images to dockerhub

build_and_push.sh present inside scripts folder uses the provide docker username and token and builds the image with name devops-app if name is not provided and  also tag latest if external name is not provided.
Once built it is then pushed to docker hub.




## Github actions workflow

Whenever there is some push into main branch of the repo.
Workflow will be triggered which first checkout the latest commit and then authenticates to GCP via  Workload Identity Federation(WIF) using the service account created.
Then gcloud auth-plugin will be installed for authentiation and cluster will be selected based on the projectID will be selected.Which inturn stores kubeconfig to connect to the cluster.
Now all required authentication are completed, next step is building a docker image from files present inside app folder and pushing it into docker hub.
Once pushed kubectl commands will be used to deploy the resources(deployment and service) into cluster.


