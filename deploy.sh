#!/bin/bash

set -e  # Exit immediately if a command fails


# ------------------------------
# Function: Check if a command exists
# ------------------------------
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if Azure CLI is installed
if ! command_exists az; then
    echo "❌ Azure CLI (az) is not installed. Please install it and try again."
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please create it and define the required variables."
    exit 1
fi

# Load environment variables
echo "🔄 Loading environment variables..."
source .env

# Required environment variables
REQUIRED_VARS=("SECRET_KEY" "ALGORITHM" "ACCESS_TOKEN_EXPIRE_MINUTES" "DB_PASSWORD")
for var in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!var}" ]; then
        echo "❌ Error: Environment variable $var is not set."
        exit 1
    fi
done

# ------------------------------
# Variables
# ------------------------------
RESOURCE_GROUP="skabdaniRG"
CONTAINER_NAME="skabdani-fastapi-loan-container-autodeploy"
ACR_NAME="skabdaniregestry"
ACR_IMAGE="bddfastapi:latest"
ACR_URL="$ACR_NAME.azurecr.io"
CPU="2"
MEMORY="8"
PORT="8000"
IP_ADDRESS="Public"
OS_TYPE="Linux"


# ------------------------------
# Azure Authentication Check
# ------------------------------
if ! az account show >/dev/null 2>&1; then
    echo "❌ Error: You are not logged into Azure. Run 'az login' and try again."
    exit 1
fi

# ------------------------------
# Get Azure Container Registry Credentials
# ------------------------------
echo "🔄 Fetching Azure Container Registry credentials..."
ACR_USERNAME=$(az acr credential show --name "$ACR_NAME" --query "username" -o tsv)
ACR_PASSWORD=$(az acr credential show --name "$ACR_NAME" --query "passwords[0].value" -o tsv)

if [ -z "$ACR_USERNAME" ] || [ -z "$ACR_PASSWORD" ]; then
    echo "❌ Error: Failed to retrieve ACR credentials."
    exit 1
fi

# ------------------------------
# Delete Existing Container (If It Exists)
# ------------------------------
if az container show --name "$CONTAINER_NAME" --resource-group "$RESOURCE_GROUP" >/dev/null 2>&1; then
    echo "🗑️ Deleting existing container: $CONTAINER_NAME..."
    az container delete --name "$CONTAINER_NAME" --resource-group "$RESOURCE_GROUP" --yes
else
    echo "ℹ️ No existing container found. Skipping deletion."
fi

# ------------------------------
# Deploy the New Container
# ------------------------------
echo "🚀 Deploying container: $CONTAINER_NAME..."
az container create \
    --name "$CONTAINER_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --image "$ACR_URL/$ACR_IMAGE" \
    --cpu "$CPU" \
    --memory "$MEMORY" \
    --registry-login-server "$ACR_URL" \
    --registry-username "$ACR_USERNAME" \
    --registry-password "$ACR_PASSWORD" \
    --ports "$PORT" \
    --ip-address "$IP_ADDRESS" \
    --os-type "$OS_TYPE" \
    --environment-variables \
        SECRET_KEY="$SECRET_KEY" \
        ALGORITHM="$ALGORITHM" \
        ACCESS_TOKEN_EXPIRE_MINUTES="$ACCESS_TOKEN_EXPIRE_MINUTES" \
        PASSWORD="$DB_PASSWORD" 

if [ $? -eq 0 ]; then
    echo "✅ Deployment successful!"
else
    echo "❌ Deployment failed!"
    exit 1
fi