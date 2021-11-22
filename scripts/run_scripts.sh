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

#   /usr/bin/ssh -t -i /Users/t966176/.ssh/google_compute_engine -o CheckHostIP=no -o HostKeyAlias=compute.4048442094882642257 -o IdentitiesOnly=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/Users/t966176/.ssh/google_compute_known_hosts -o ProxyCommand="C:\Users\t966176\Documents\workfolder\google-cloud-sdk\platform\bundledpython\python.exe -S C:\Users\t966176\Documents\workfolder\google-cloud-sdk\lib\gcloud.py" compute start-iap-tunnel test-ssh-vs %p --listen-on-stdin --project=atoosa-wb-v2-pr-656b47 --zone=northamerica-northeast1-a --verbosity=warning" -o ProxyUseFdpass=no