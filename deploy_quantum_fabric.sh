#!/bin/bash
set -e # Exit immediately if a command exits with a non-zero status.

echo "========================================="
echo "  COMMANDER QUANTUM FABRIC DEPLOYMENT    "
echo "========================================="

# 1. Authenticate with Cloud Provider
echo "[PHASE 1/5] Authenticating with Google Cloud..."
gcloud auth login
gcloud auth application-default login
PROJECT_ID=$(gcloud config get-value project)
echo "Authentication successful for project: $PROJECT_ID"

# 2. Enable necessary APIs
echo "[PHASE 2/5] Enabling required temporal and AI APIs..."
gcloud services enable aiplatform.googleapis.com
gcloud services enable container.googleapis.com
gcloud services enable cloudbuild.googleapis.com
echo "APIs enabled."

# 3. Deploy Terraform Infrastructure
echo "[PHASE 3/5] Deploying Terraform infrastructure (VPC, QPU Links, ChronosDB)..."
cd ./terraform
terraform init
terraform apply -auto-approve -var="project_id=$PROJECT_ID"
echo "Terraform fabric deployed."
cd ..

# 4. Build and deploy the Orchestrator container
echo "[PHASE 4/5] Building and deploying Orchestrator service..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/commander-orchestrator:latest .
gcloud run deploy commander-orchestrator \
    --image=gcr.io/$PROJECT_ID/commander-orchestrator:latest \
    --platform=managed \
    --region=us-central1 \
    --allow-unauthenticated \
    --set-env-vars="CHRONOS_API_TOKEN=$CHRONOS_API_TOKEN"
echo "Orchestrator service is live."

# 5. Sync Temporal States
echo "[PHASE 5/5] Syncing temporal states and warming up GenAI model..."
# This would call a script or endpoint to initialize the DB
curl -X POST "https://commander-orchestrator-....run.app/api/v1/system/init"
echo "Sync complete."

echo "========================================="
echo "  DEPLOYMENT SUCCESSFUL                  "
echo "  Commander is now online.               "
echo "========================================="
