#!/bin/bash

gcloud compute ssh --zone "northamerica-northeast1-a" \
 "test-ssh-vs" --tunnel-through-iap \
 --dry-run