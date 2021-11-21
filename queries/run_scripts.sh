#!/bin/bash

# https://cloud.google.com/sdk/docs/scripting-gcloud

# create a notebook from image
gcloud notebooks instances create test-ssh-vs \
    --vm-image-project=deeplearning-platform-release \
    --vm-image-family=caffe1-latest-cpu-experimental \
    --machine-type=n1-standard-4 \
    --location=northamerica-northeast1-a \
    --network=atoosa-wb-v2-pr-656b47-network \
    --no-public-ip \
    --subnet=default-subnet-pr \
    --subnet-region=northamerica-northeast1
    
    # --service-account=66950319389-compute@developer.gserviceaccount.com