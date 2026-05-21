pipeline {
  agent any

  environment {
    REGION = 'us-central1'
    IMAGE_NAME = 'devops-app'
    CLUSTER_NAME = 'devops-cluster'
    GKE_REGION = 'us-central1'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Verify tools') {
      steps {
        sh '''
          echo "Checking required CLI tools..."
          command -v docker >/dev/null 2>&1 || { echo "docker is missing"; exit 1; }
          command -v gcloud >/dev/null 2>&1 || { echo "gcloud is missing"; exit 1; }
          command -v kubectl >/dev/null 2>&1 || { echo "kubectl is missing"; exit 1; }
          docker --version
          gcloud --version
          kubectl version --client
        '''
      }
    }

    stage('Build and Push') {
      steps {
        withCredentials([
          string(credentialsId: 'dockerhub-username', variable: 'DOCKERHUB_USERNAME'),
          string(credentialsId: 'dockerhub-token', variable: 'DOCKERHUB_TOKEN')
        ]) {
          sh '''
            export IMAGE_TAG="$(echo "$GIT_COMMIT" | cut -c1-7)"
            export IMAGE="docker.io/${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG}"
            export IMAGE_OUTPUT_FILE="image.env"
            chmod +x ./scripts/build_and_push.sh
            ./scripts/build_and_push.sh
          '''
        }
      }
    }

    stage('Authenticate to GCP') {
      steps {
        withCredentials([
          string(credentialsId: 'gcp-project-id', variable: 'GCP_PROJECT_ID'),
          string(credentialsId: 'gcp-workload-identity-provider', variable: 'GCP_WORKLOAD_ID_PROVIDER'),
          string(credentialsId: 'gcp-service-account-email', variable: 'GCP_SA_EMAIL'),
          string(credentialsId: 'workload-identity-token', variable: 'WORKLOAD_ID_TOKEN')
        ]) {
          sh '''
            cat > /tmp/wif-config.json <<'EOF'
            {
              "type": "external_account",
              "audience": "${GCP_WORKLOAD_ID_PROVIDER}",
              "subject_token_type": "urn:ietf:params:oauth:token-type:jwt",
              "token_url": "https://sts.googleapis.com/v1/token",
              "service_account_impersonation_url": "https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/${GCP_SA_EMAIL}:generateAccessToken",
              "credential_source": {
                "file": "/tmp/workload-identity-token.jwt"
              }
            }
            EOF

            echo "${WORKLOAD_ID_TOKEN}" > /tmp/workload-identity-token.jwt
            gcloud auth activate-service-account --key-file=/tmp/wif-config.json --project="${GCP_PROJECT_ID}"
            gcloud config set project "${GCP_PROJECT_ID}"
          '''
        }
      }
    }

    stage('Deploy to GKE') {
      steps {
        withCredentials([
          string(credentialsId: 'gcp-project-id', variable: 'GCP_PROJECT_ID')
        ]) {
          sh '''
            gcloud config set account praveenmp6793@gmail.com
            gcloud container clusters get-credentials "$CLUSTER_NAME" --region "$GKE_REGION" --project "$GCP_PROJECT_ID"
            source image.env
            kubectl apply -f k8s/namespace.yaml
            kubectl apply -f k8s/
            kubectl set image deployment/devops-app app="$IMAGE" -n devops
            kubectl rollout status deployment/devops-app -n devops
            echo "Deployment complete with image $IMAGE"
          '''
        }
      }
    }
  }

  post {
    always {
      sh 'docker logout || true'
    }
  }
}
